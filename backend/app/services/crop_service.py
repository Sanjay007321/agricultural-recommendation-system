import json
import os
from typing import Dict, List, Optional
from app.models.schemas import AnalysisInput

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

def load_crops_data():
    with open(os.path.join(DATA_PATH, "crops.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def get_crop_by_name(crop_name: str) -> Optional[Dict]:
    """Get crop details by crop name"""
    crops_data = load_crops_data()
    crops = crops_data.get("crops", [])
    
    for crop in crops:
        if crop["name"].lower() == crop_name.lower():
            return crop
    return None

def get_crop_varieties(crop_name: str) -> List[Dict]:
    """Get all varieties for a specific crop"""
    crop = get_crop_by_name(crop_name)
    if crop:
        return crop.get("varieties", [])
    return []

def get_crop_suitable_lands(crop_name: str) -> List[str]:
    """Get suitable lands for a crop"""
    crop = get_crop_by_name(crop_name)
    if crop:
        return crop.get("suitable_lands", [])
    return []

def get_variety_details(crop_name: str, variety_name: str) -> Optional[Dict]:
    """Get details of a specific crop variety"""
    varieties = get_crop_varieties(crop_name)
    for variety in varieties:
        if variety["name"].lower() == variety_name.lower():
            return variety
    return None

def calculate_soil_score(crop: Dict, input_data: AnalysisInput) -> float:
    """Calculate how well the soil matches crop requirements"""
    score = 0.0
    
    # Soil type match
    if input_data.soil_type in crop.get("soil_types", []):
        score += 30
    
    # pH match
    ph_range = crop.get("ph_range", [6.0, 7.5])
    if ph_range[0] <= input_data.soil_ph <= ph_range[1]:
        score += 20
    elif abs(input_data.soil_ph - sum(ph_range)/2) < 1:
        score += 10
    
    # NPK match
    n_req = crop.get("nitrogen_required", 100)
    p_req = crop.get("phosphorus_required", 50)
    k_req = crop.get("potassium_required", 50)
    
    if input_data.nitrogen >= n_req * 0.8:
        score += 10
    if input_data.phosphorus >= p_req * 0.8:
        score += 10
    if input_data.potassium >= k_req * 0.8:
        score += 10
    
    return score

def calculate_climate_score(crop: Dict, input_data: AnalysisInput) -> float:
    """Calculate how well climate matches crop requirements"""
    score = 0.0
    
    # Season match
    if input_data.season in crop.get("season", []):
        score += 30
    
    # Temperature match
    temp_range = crop.get("temperature_range", [15, 35])
    if temp_range[0] <= input_data.temperature_c <= temp_range[1]:
        score += 20
    elif abs(input_data.temperature_c - sum(temp_range)/2) < 5:
        score += 10
    
    # Rainfall match
    rain_range = crop.get("rainfall_mm", [500, 1500])
    if rain_range[0] <= input_data.rainfall_mm <= rain_range[1]:
        score += 20
    elif rain_range[0] * 0.7 <= input_data.rainfall_mm <= rain_range[1] * 1.3:
        score += 10
    
    return score

def get_best_variety(crop: Dict, input_data: AnalysisInput) -> Optional[Dict]:
    """Select the best variety for the crop based on input conditions"""
    varieties = crop.get("varieties", [])
    if not varieties:
        return None
    
    best_variety = None
    best_score = -1
    
    for variety in varieties:
        score = 0
        
        # Score based on rainfall match
        water_req = variety.get("water_requirement", "")
        if "High" in water_req and input_data.rainfall_mm >= 1200:
            score += 35
        elif "Medium-High" in water_req and 1000 <= input_data.rainfall_mm < 1500:
            score += 35
        elif "Medium" in water_req and 800 <= input_data.rainfall_mm < 1200:
            score += 35
        elif input_data.rainfall_mm >= 500:
            score += 15
        
        # Score based on characteristics and suitability
        best_for = variety.get("best_for", "").lower()
        if "rainfed" in best_for and input_data.rainfall_mm < 800:
            score += 20
        elif "irrigated" in best_for and input_data.rainfall_mm >= 1000:
            score += 20
        elif "marginal" in best_for and input_data.budget_inr < 50000:
            score += 15
        
        if score > best_score:
            best_score = score
            best_variety = variety
    
    return best_variety if best_variety and best_score > 0 else (varieties[0] if varieties else None)

def get_crop_recommendation(input_data: AnalysisInput) -> Dict:
    """
    Recommend best crop based on soil and climate conditions
    Uses rule-based scoring (can be replaced with ML model)
    """
    crops_data = load_crops_data()
    crops = crops_data.get("crops", [])
    
    crop_scores = []
    
    for crop in crops:
        soil_score = calculate_soil_score(crop, input_data)
        climate_score = calculate_climate_score(crop, input_data)
        
        # Total score out of 100
        total_score = (soil_score + climate_score) / 1.2
        
        crop_scores.append({
            "name": crop["name"],
            "score": total_score,
            "soil_score": soil_score,
            "climate_score": climate_score,
            "crop_data": crop
        })
    
    # Sort by score
    crop_scores.sort(key=lambda x: x["score"], reverse=True)
    
    # Get top recommendation
    top_crop = crop_scores[0]
    
    # Get best variety for recommended crop
    best_variety = get_best_variety(top_crop["crop_data"], input_data)
    
    # Generate reasoning
    reasoning_parts = []
    if top_crop["soil_score"] >= 50:
        reasoning_parts.append(f"{input_data.soil_type} soil with pH {input_data.soil_ph} is ideal")
    if top_crop["climate_score"] >= 50:
        reasoning_parts.append(f"{input_data.season} season with {input_data.rainfall_mm}mm rainfall suits well")
    
    reasoning = f"{top_crop['name']} recommended because: " + ", ".join(reasoning_parts) if reasoning_parts else f"{top_crop['name']} is the best match for given conditions"
    
    result = {
        "recommended_crop": top_crop["name"],
        "recommended_variety": best_variety.get("name") if best_variety else None,
        "confidence": round(top_crop["score"] / 100, 2),
        "suitable_lands": top_crop["crop_data"].get("suitable_lands", []),
        "alternatives": [
            {
                "crop": crop_scores[1]["name"],
                "confidence": round(crop_scores[1]["score"] / 100, 2),
                "suitable_lands": crop_scores[1]["crop_data"].get("suitable_lands", [])
            },
            {
                "crop": crop_scores[2]["name"],
                "confidence": round(crop_scores[2]["score"] / 100, 2),
                "suitable_lands": crop_scores[2]["crop_data"].get("suitable_lands", [])
            }
        ] if len(crop_scores) >= 3 else [],
        "reasoning": reasoning
    }
    
    if best_variety:
        result["variety_details"] = {
            "name": best_variety.get("name"),
            "duration": best_variety.get("duration"),
            "yield": best_variety.get("yield_quintal_acre"),
            "price": best_variety.get("price_per_quintal"),
            "characteristics": best_variety.get("characteristics"),
            "water_requirement": best_variety.get("water_requirement"),
            "best_for": best_variety.get("best_for")
        }
    
    return result
