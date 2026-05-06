import json
import os
from typing import Dict, List
from app.models.schemas import AnalysisInput
from app.models.user import User

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

def load_schemes_data():
    with open(os.path.join(DATA_PATH, "schemes.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def check_eligibility(scheme: Dict, user: User, input_data: AnalysisInput) -> bool:
    """Check if farmer is eligible for a scheme"""
    eligibility = scheme.get("eligibility", {})
    
    # If all farmers are eligible
    if eligibility.get("all_farmers", False):
        return True
    
    # Check land size limit
    land_max = eligibility.get("land_size_max_acres")
    if land_max and user.land_size_acres:
        if user.land_size_acres > land_max:
            return False
    
    # Check if scheme is for specific crops
    scheme_crops = eligibility.get("crops", [])
    if scheme_crops:
        # Check if user's crop preference matches
        crop_pref = input_data.crop_preference or ""
        if crop_pref.lower() != "auto" and crop_pref not in scheme_crops:
            return False
    
    # Check oilseed schemes
    if eligibility.get("oilseed_farmers"):
        oilseeds = ["Groundnut", "Soybean", "Sunflower", "Mustard", "Sesame"]
        crop_pref = input_data.crop_preference or ""
        if crop_pref.lower() != "auto" and crop_pref not in oilseeds:
            return False
    
    # Check horticulture schemes
    if eligibility.get("horticulture_farmers"):
        # Simplified check
        horticulture = ["Tomato", "Onion", "Potato", "Chilli", "Turmeric"]
        crop_pref = input_data.crop_preference or ""
        if crop_pref.lower() != "auto" and crop_pref not in horticulture:
            return False
    
    return True

def get_eligible_schemes(user: User, input_data: AnalysisInput) -> List[Dict]:
    """
    Get list of government schemes the farmer is eligible for
    """
    schemes_data = load_schemes_data()
    all_schemes = schemes_data.get("schemes", [])
    
    eligible_schemes = []
    
    for scheme in all_schemes:
        if check_eligibility(scheme, user, input_data):
            eligible_schemes.append({
                "name": scheme["name"],
                "benefit": scheme["benefit"],
                "eligibility": "Eligible" if check_eligibility(scheme, user, input_data) else "Check eligibility",
                "apply_link": scheme.get("apply_link"),
                "helpline": scheme.get("helpline")
            })
    
    # Sort by most relevant (PM-KISAN and PMFBY first)
    priority_schemes = ["PM-KISAN", "PMFBY", "Kisan Credit Card", "Soil Health Card"]
    
    def sort_key(s):
        try:
            return priority_schemes.index(s["name"])
        except ValueError:
            return 100
    
    eligible_schemes.sort(key=sort_key)
    
    # Return top 6 most relevant
    return eligible_schemes[:6]

def get_all_schemes() -> List[Dict]:
    """Get all government schemes"""
    schemes_data = load_schemes_data()
    return schemes_data.get("schemes", [])
