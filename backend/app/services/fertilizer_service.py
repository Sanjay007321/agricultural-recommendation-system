import json
import os
from typing import Dict, List
from app.models.schemas import AnalysisInput

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

def load_crops_data():
    with open(os.path.join(DATA_PATH, "crops.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def load_fertilizers_data():
    with open(os.path.join(DATA_PATH, "fertilizers.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def get_crop_info(crop_name: str) -> Dict:
    crops_data = load_crops_data()
    for crop in crops_data.get("crops", []):
        if crop["name"].lower() == crop_name.lower():
            return crop
    return None

def calculate_npk_deficit(crop: Dict, input_data: AnalysisInput) -> Dict:
    """Calculate NPK deficit based on crop requirements and soil levels"""
    n_required = crop.get("nitrogen_required", 100)
    p_required = crop.get("phosphorus_required", 50)
    k_required = crop.get("potassium_required", 50)
    
    # Calculate deficit (what needs to be added)
    n_deficit = max(0, n_required - input_data.nitrogen)
    p_deficit = max(0, p_required - input_data.phosphorus)
    k_deficit = max(0, k_required - input_data.potassium)
    
    return {
        "nitrogen": n_deficit,
        "phosphorus": p_deficit,
        "potassium": k_deficit
    }

def get_fertilizer_recommendation(crop_name: str, input_data: AnalysisInput) -> Dict:
    """
    Generate fertilizer recommendations based on crop needs and soil conditions
    Uses XGBoost model (simulated with rule-based logic)
    """
    crop = get_crop_info(crop_name)
    fertilizers_data = load_fertilizers_data()
    fertilizers = fertilizers_data.get("fertilizers", [])
    
    recommendations = []
    total_cost = 0
    
    if not crop:
        # Default recommendation
        return {
            "recommendations": [
                {
                    "name": "DAP",
                    "quantity_kg_per_acre": 50,
                    "cost_inr": 1350,
                    "timing": "At sowing"
                },
                {
                    "name": "Urea",
                    "quantity_kg_per_acre": 50,
                    "cost_inr": 700,
                    "timing": "Top dressing at 30 days"
                }
            ],
            "total_cost": 2050 * input_data.land_area_acres
        }
    
    # Calculate NPK deficit
    deficit = calculate_npk_deficit(crop, input_data)
    
    # DAP for phosphorus (also provides some nitrogen)
    if deficit["phosphorus"] > 0:
        dap_qty = min(deficit["phosphorus"] / 0.46, 100)  # 46% P in DAP
        dap_cost = dap_qty * 27  # Rs 27/kg
        recommendations.append({
            "name": "DAP",
            "quantity_kg_per_acre": round(dap_qty, 1),
            "cost_inr": round(dap_cost, 0),
            "timing": "At sowing/transplanting"
        })
        total_cost += dap_cost
        # DAP provides 18% N, adjust nitrogen deficit
        deficit["nitrogen"] -= dap_qty * 0.18
    
    # Urea for remaining nitrogen
    if deficit["nitrogen"] > 0:
        urea_qty = min(deficit["nitrogen"] / 0.46, 100)  # 46% N in Urea
        urea_cost = urea_qty * 14  # Rs 14/kg
        recommendations.append({
            "name": "Urea",
            "quantity_kg_per_acre": round(urea_qty, 1),
            "cost_inr": round(urea_cost, 0),
            "timing": "Top dressing in 2-3 splits"
        })
        total_cost += urea_cost
    
    # MOP for potassium
    if deficit["potassium"] > 0:
        mop_qty = min(deficit["potassium"] / 0.60, 50)  # 60% K in MOP
        mop_cost = mop_qty * 20  # Rs 20/kg
        recommendations.append({
            "name": "MOP",
            "quantity_kg_per_acre": round(mop_qty, 1),
            "cost_inr": round(mop_cost, 0),
            "timing": "At sowing"
        })
        total_cost += mop_cost
    
    # Zinc sulphate for rice, wheat
    if crop_name.lower() in ["rice", "wheat", "maize"]:
        recommendations.append({
            "name": "Zinc Sulphate",
            "quantity_kg_per_acre": 10,
            "cost_inr": 450,
            "timing": "At sowing or foliar spray"
        })
        total_cost += 450
    
    # If no deficit, recommend basic maintenance
    if not recommendations:
        recommendations = [
            {
                "name": "NPK 10-26-26",
                "quantity_kg_per_acre": 40,
                "cost_inr": 1280,
                "timing": "At sowing"
            }
        ]
        total_cost = 1280
    
    # Multiply by land area
    total_cost = total_cost * input_data.land_area_acres
    
    return {
        "recommendations": recommendations,
        "total_cost": round(total_cost, 0)
    }
