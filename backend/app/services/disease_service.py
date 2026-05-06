import json
import os
from typing import Dict, List
from app.models.schemas import AnalysisInput

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

def load_pesticides_data():
    with open(os.path.join(DATA_PATH, "pesticides.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def calculate_disease_risk(input_data: AnalysisInput) -> str:
    """
    Calculate disease risk level based on environmental conditions
    Uses Random Forest model (simulated)
    """
    humidity = input_data.humidity_percent or 60
    rainfall = input_data.rainfall_mm
    temperature = input_data.temperature_c
    
    risk_score = 0
    
    # High humidity increases disease risk
    if humidity > 80:
        risk_score += 40
    elif humidity > 65:
        risk_score += 20
    
    # High rainfall increases fungal disease risk
    if rainfall > 1500:
        risk_score += 30
    elif rainfall > 1000:
        risk_score += 15
    
    # Moderate temperatures with humidity increase risk
    if 20 <= temperature <= 30 and humidity > 70:
        risk_score += 20
    
    # Kharif season has higher pest pressure
    if input_data.season == "Kharif":
        risk_score += 10
    
    if risk_score >= 60:
        return "High"
    elif risk_score >= 30:
        return "Medium"
    else:
        return "Low"

def get_crop_diseases(crop_name: str) -> List[Dict]:
    """Get common diseases for a crop"""
    pesticides_data = load_pesticides_data()
    diseases = pesticides_data.get("diseases", {})
    
    crop_diseases = diseases.get(crop_name, [])
    
    # If crop not found, return generic diseases
    if not crop_diseases:
        return [
            {
                "name": "Leaf Spot",
                "symptoms": ["Brown spots on leaves", "Yellowing"],
                "pesticides": ["Mancozeb", "Copper oxychloride"]
            },
            {
                "name": "Root Rot",
                "symptoms": ["Wilting", "Yellowing", "Root decay"],
                "pesticides": ["Carbendazim", "Trichoderma"]
            }
        ]
    
    return crop_diseases

def get_pesticide_info(pesticide_name: str) -> Dict:
    """Get pesticide details"""
    pesticides_data = load_pesticides_data()
    for pest in pesticides_data.get("pesticides", []):
        if pest["name"].lower() == pesticide_name.lower():
            return pest
    return None

def get_disease_risk(crop_name: str, input_data: AnalysisInput) -> Dict:
    """
    Analyze disease risk and recommend pesticides
    Uses Random Forest model (simulated)
    """
    risk_level = calculate_disease_risk(input_data)
    crop_diseases = get_crop_diseases(crop_name)
    
    # Select likely diseases based on risk level
    likely_diseases = []
    pesticide_recommendations = []
    total_cost = 0
    
    # Number of diseases to warn about based on risk
    num_diseases = {"High": 3, "Medium": 2, "Low": 1}.get(risk_level, 1)
    
    for disease in crop_diseases[:num_diseases]:
        likely_diseases.append(disease["name"])
        
        # Get pesticide recommendations for this disease
        for pest_name in disease.get("pesticides", [])[:2]:
            pest_info = get_pesticide_info(pest_name)
            
            if pest_info:
                # Calculate cost per acre (assuming 200L spray solution per acre)
                if "price_per_100ml" in pest_info:
                    cost = pest_info["price_per_100ml"] * 10  # For 1L
                elif "price_per_100g" in pest_info:
                    cost = pest_info["price_per_100g"] * 5  # For 500g
                else:
                    cost = 500  # Default
                
                pesticide_recommendations.append({
                    "name": pest_name,
                    "dosage": pest_info.get("dosage", "As per label"),
                    "timing": "When symptoms appear" if risk_level == "Low" else "Preventive spray recommended",
                    "cost_inr": round(cost, 0)
                })
                total_cost += cost
    
    # Remove duplicates
    seen = set()
    unique_pesticides = []
    for p in pesticide_recommendations:
        if p["name"] not in seen:
            seen.add(p["name"])
            unique_pesticides.append(p)
    
    # Add neem oil as organic option
    if risk_level != "Low":
        unique_pesticides.append({
            "name": "Neem Oil",
            "dosage": "5 ml/L",
            "timing": "Every 15 days as preventive",
            "cost_inr": 350
        })
        total_cost += 350
    
    # Multiply cost by land area
    total_cost = total_cost * input_data.land_area_acres
    
    return {
        "risk_level": risk_level,
        "diseases": likely_diseases,
        "pesticides": unique_pesticides,
        "total_cost": round(total_cost, 0)
    }
