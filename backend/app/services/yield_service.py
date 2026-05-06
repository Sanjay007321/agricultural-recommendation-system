import json
import os
import numpy as np
from typing import Dict
from app.models.schemas import AnalysisInput

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

def load_crops_data():
    with open(os.path.join(DATA_PATH, "crops.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def get_crop_info(crop_name: str) -> Dict:
    """Get crop information from data"""
    crops_data = load_crops_data()
    for crop in crops_data.get("crops", []):
        if crop["name"].lower() == crop_name.lower():
            return crop
    return None

def calculate_yield_factors(crop: Dict, input_data: AnalysisInput) -> float:
    """
    Calculate yield adjustment factors based on conditions
    Returns multiplier (0.5 to 1.2)
    """
    factor = 1.0
    
    # Soil type factor
    if input_data.soil_type in crop.get("soil_types", []):
        factor *= 1.05
    else:
        factor *= 0.85
    
    # pH factor
    ph_range = crop.get("ph_range", [6.0, 7.5])
    optimal_ph = sum(ph_range) / 2
    ph_deviation = abs(input_data.soil_ph - optimal_ph)
    if ph_deviation < 0.5:
        factor *= 1.05
    elif ph_deviation < 1.0:
        factor *= 0.95
    else:
        factor *= 0.85
    
    # NPK factor
    n_req = crop.get("nitrogen_required", 100)
    p_req = crop.get("phosphorus_required", 50)
    k_req = crop.get("potassium_required", 50)
    
    n_ratio = min(input_data.nitrogen / n_req, 1.2)
    p_ratio = min(input_data.phosphorus / p_req, 1.2)
    k_ratio = min(input_data.potassium / k_req, 1.2)
    
    npk_factor = (n_ratio + p_ratio + k_ratio) / 3
    factor *= (0.7 + 0.3 * npk_factor)
    
    # Temperature factor
    temp_range = crop.get("temperature_range", [15, 35])
    if temp_range[0] <= input_data.temperature_c <= temp_range[1]:
        factor *= 1.0
    else:
        factor *= 0.85
    
    # Rainfall factor
    rain_range = crop.get("rainfall_mm", [500, 1500])
    if rain_range[0] <= input_data.rainfall_mm <= rain_range[1]:
        factor *= 1.0
    elif rain_range[0] * 0.7 <= input_data.rainfall_mm <= rain_range[1] * 1.3:
        factor *= 0.9
    else:
        factor *= 0.75
    
    return min(max(factor, 0.5), 1.2)

def predict_yield(crop_name: str, input_data: AnalysisInput) -> Dict:
    """
    Predict crop yield using LSTM model (simulated)
    Returns expected yield per acre and total yield
    """
    crop = get_crop_info(crop_name)
    
    if not crop:
        # Default values if crop not found
        base_yield = 15
    else:
        base_yield = crop.get("avg_yield_quintal_per_acre", 15)
    
    # Calculate adjustment factor
    if crop:
        yield_factor = calculate_yield_factors(crop, input_data)
    else:
        yield_factor = 0.9
    
    # Predicted yield per acre
    expected_per_acre = base_yield * yield_factor
    
    # Total yield based on land area
    total_yield = expected_per_acre * input_data.land_area_acres
    
    # Confidence range (±15%)
    confidence_range = [
        round(total_yield * 0.85, 1),
        round(total_yield * 1.15, 1)
    ]
    
    return {
        "expected_per_acre": round(expected_per_acre, 1),
        "total_yield_quintal": round(total_yield, 1),
        "confidence_range": confidence_range,
        "yield_factor": round(yield_factor, 2)
    }
