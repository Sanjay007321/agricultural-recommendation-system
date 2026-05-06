"""
Irrigation Planning Service - Provides crop-specific irrigation recommendations
"""

from typing import Dict, List
from app.models.schemas import AnalysisInput
from app.services.crop_service import get_crop_by_name

def get_irrigation_planning(crop_name: str, input_data: AnalysisInput) -> Dict:
    """
    Generate detailed irrigation planning recommendations based on crop and conditions
    """
    
    # Get crop data
    crop = get_crop_by_name(crop_name)
    if not crop:
        return get_default_irrigation()
    
    # Extract crop water requirements
    crop_water_req = crop.get("rainfall_mm", [600, 1200])
    min_water = crop_water_req[0] if isinstance(crop_water_req, list) else 600
    max_water = crop_water_req[1] if isinstance(crop_water_req, list) else 1200
    
    # Calculate irrigation need based on rainfall
    rainfall = input_data.rainfall_mm
    irrigation_required = max(0, min_water - rainfall)
    
    # Determine irrigation method based on factors
    irrigation_method = determine_irrigation_method(crop_name, input_data, irrigation_required)
    
    # Generate irrigation schedule
    schedule = generate_irrigation_schedule(crop_name, input_data)
    
    # Generate water management tips
    tips = generate_water_tips(crop_name, irrigation_required, input_data)
    
    # Calculate irrigation cost
    irrigation_cost = calculate_irrigation_cost(irrigation_method, schedule, input_data)
    
    return {
        "irrigation_required_mm": round(irrigation_required, 2),
        "total_water_needed_mm": round(min_water, 2),
        "rainfall_mm": rainfall,
        "irrigation_method": irrigation_method,
        "irrigation_schedule": schedule,
        "water_management_tips": tips,
        "estimated_cost_per_acre": irrigation_cost,
        "efficiency_percentage": calculate_irrigation_efficiency(irrigation_method)
    }


def determine_irrigation_method(crop_name: str, input_data: AnalysisInput, irrigation_required: float) -> str:
    """Determine best irrigation method based on crop and land area"""
    
    # High water requirement crops
    high_water_crops = ["Rice", "Sugarcane", "Tomato", "Onion"]
    
    # Medium water requirement crops
    medium_water_crops = ["Wheat", "Maize", "Cotton", "Chilli"]
    
    # Low water crops
    low_water_crops = ["Mustard", "Chickpea", "Groundnut", "Sunflower"]
    
    land_area = input_data.land_area_acres
    
    # Rules for irrigation method selection
    if crop_name in high_water_crops and irrigation_required > 500:
        if land_area > 5:
            return "Drip Irrigation (Primary) + Drip Lines with Mulch"
        else:
            return "Drip Irrigation with Micro-sprinklers"
    
    elif crop_name in medium_water_crops:
        if land_area > 10:
            return "Sprinkler Irrigation (Boom or Lateral Move)"
        elif land_area > 5:
            return "Drip Irrigation (Widely spaced crops)"
        else:
            return "Micro-sprinkler or Subsurface Drip"
    
    elif crop_name in low_water_crops:
        if irrigation_required < 200:
            return "Flood Irrigation (Furrow Method)"
        else:
            return "Drip Irrigation or Mulched Field"
    
    else:
        if irrigation_required > 400:
            return "Sprinkler Irrigation"
        elif irrigation_required > 200:
            return "Drip Irrigation"
        else:
            return "Flood Irrigation (Basin Method)"


def generate_irrigation_schedule(crop_name: str, input_data: AnalysisInput) -> List[Dict]:
    """Generate crop-specific irrigation schedule"""
    
    # Define irrigation stages for different crops
    schedules = {
        "Rice": [
            {"stage": "Land Preparation", "days_after_sowing": "0-7", "depth_mm": 50, "frequency": "Daily", "notes": "Puddle the field, maintain 2-3 cm standing water"},
            {"stage": "Vegetative Growth", "days_after_sowing": "7-60", "depth_mm": 60, "frequency": "Every 5-7 days", "notes": "Maintain 5 cm water level, ensure proper drainage"},
            {"stage": "Flowering & Grain Filling", "days_after_sowing": "60-100", "depth_mm": 50, "frequency": "Every 7-10 days", "notes": "Critical stage - ensure continuous water supply"},
            {"stage": "Maturity", "days_after_sowing": "100-120", "depth_mm": 25, "frequency": "As needed", "notes": "Reduce water, allow field to dry gradually"}
        ],
        "Wheat": [
            {"stage": "CRI (Crown Root Initiation)", "days_after_sowing": "20-25", "depth_mm": 50, "frequency": "Single", "notes": "Critical for root development"},
            {"stage": "Tillers to Boot Stage", "days_after_sowing": "40-70", "depth_mm": 50, "frequency": "Every 10-15 days", "notes": "2-3 irrigations for rainfed, 1 for irrigated"},
            {"stage": "Flowering & Grain Filling", "days_after_sowing": "70-110", "depth_mm": 50, "frequency": "Every 15-20 days", "notes": "Final 1-2 irrigations critical"},
            {"stage": "Maturity", "days_after_sowing": "110-130", "depth_mm": 0, "frequency": "None", "notes": "Stop irrigation 2 weeks before harvest"}
        ],
        "Maize": [
            {"stage": "Seedling", "days_after_sowing": "0-20", "depth_mm": 30, "frequency": "Light frequent", "notes": "Keep soil moist, avoid waterlogging"},
            {"stage": "Vegetative Growth", "days_after_sowing": "20-50", "depth_mm": 50, "frequency": "Every 7-10 days", "notes": "Critical - ensure adequate water"},
            {"stage": "Flowering & Grain Setting", "days_after_sowing": "50-75", "depth_mm": 60, "frequency": "Every 5-7 days", "notes": "Most critical stage for yield"},
            {"stage": "Grain Filling", "days_after_sowing": "75-100", "depth_mm": 40, "frequency": "Every 10-15 days", "notes": "Reduce frequency gradually"}
        ],
        "Cotton": [
            {"stage": "Seedling to Branching", "days_after_sowing": "0-45", "depth_mm": 35, "frequency": "Every 7-10 days", "notes": "Light irrigation, good drainage essential"},
            {"stage": "Flowering & Boll Formation", "days_after_sowing": "45-120", "depth_mm": 45, "frequency": "Every 10-15 days", "notes": "Most critical - 4-6 irrigations"},
            {"stage": "Boll Maturity", "days_after_sowing": "120-180", "depth_mm": 30, "frequency": "Every 15-20 days", "notes": "Reduce water, promote ripening"}
        ],
        "Sugarcane": [
            {"stage": "Establishment (0-4 months)", "days_after_sowing": "0-120", "depth_mm": 80, "frequency": "Every 10-15 days", "notes": "12-14 irrigations, critical for shoot growth"},
            {"stage": "Rapid Growth (4-8 months)", "days_after_sowing": "120-240", "depth_mm": 90, "frequency": "Every 15-20 days", "notes": "Heavy watering period, 10-12 irrigations"},
            {"stage": "Maturity (8-12 months)", "days_after_sowing": "240-365", "depth_mm": 70, "frequency": "Every 20-30 days", "notes": "Stop 4-6 weeks before harvest for better quality"}
        ],
        "Tomato": [
            {"stage": "Seedling to Transplanting", "days_after_sowing": "0-30", "depth_mm": 25, "frequency": "Daily light", "notes": "Keep soil moist, mulch recommended"},
            {"stage": "Vegetative Growth", "days_after_sowing": "30-60", "depth_mm": 40, "frequency": "Every 5-7 days", "notes": "Drip irrigation preferred"},
            {"stage": "Flowering & Fruiting", "days_after_sowing": "60-90", "depth_mm": 50, "frequency": "Every 3-5 days", "notes": "Critical stage - consistent watering"},
            {"stage": "Harvest", "days_after_sowing": "90+", "depth_mm": 40, "frequency": "Every 5-7 days", "notes": "Continue until end of season"}
        ],
        "Onion": [
            {"stage": "Initial Growth (Bulb Formation begins)", "days_after_sowing": "0-60", "depth_mm": 35, "frequency": "Every 7-10 days", "notes": "Maintain optimal soil moisture"},
            {"stage": "Active Bulb Growth", "days_after_sowing": "60-100", "depth_mm": 45, "frequency": "Every 5-7 days", "notes": "Critical period for bulb size"},
            {"stage": "Bulb Maturity", "days_after_sowing": "100-120", "depth_mm": 25, "frequency": "Every 15-20 days", "notes": "Reduce water for bulb curing"}
        ],
        "Groundnut": [
            {"stage": "Seedling Stage", "days_after_sowing": "0-30", "depth_mm": 30, "frequency": "Every 7-10 days", "notes": "Light irrigation for germination"},
            {"stage": "Vegetative Growth", "days_after_sowing": "30-70", "depth_mm": 40, "frequency": "Every 10-15 days", "notes": "2-3 irrigations sufficient for rainfed"},
            {"stage": "Flowering & Pod Dev", "days_after_sowing": "70-110", "depth_mm": 50, "frequency": "Every 10-15 days", "notes": "Important growth stage"},
            {"stage": "Pod Maturity", "days_after_sowing": "110-120", "depth_mm": 0, "frequency": "Minimal", "notes": "Stop irrigation to aid pod maturation"}
        ]
    }
    
    # Return crop-specific schedule or default
    return schedules.get(crop_name, get_default_schedule())


def get_default_schedule() -> List[Dict]:
    """Default irrigation schedule for crops not specifically defined"""
    return [
        {"stage": "Initial Growth", "days_after_sowing": "0-30", "depth_mm": 35, "frequency": "Every 7-10 days", "notes": "Keep soil consistently moist"},
        {"stage": "Active Growth", "days_after_sowing": "30-80", "depth_mm": 50, "frequency": "Every 10-15 days", "notes": "Increase water supply"},
        {"stage": "Flowering/Fruiting", "days_after_sowing": "80-120", "depth_mm": 50, "frequency": "Every 10-15 days", "notes": "Maintain consistent moisture"},
        {"stage": "Maturity", "days_after_sowing": "120+", "depth_mm": 30, "frequency": "Every 15-20 days", "notes": "Reduce gradually towards harvest"}
    ]


def generate_water_tips(crop_name: str, irrigation_required: float, input_data: AnalysisInput) -> List[str]:
    """Generate water management best practices"""
    
    tips = []
    
    # Based on irrigation requirement
    if irrigation_required > 500:
        tips.append("High water requirement crop - Plan for reliable water source")
        tips.append("Consider water harvesting or pond construction for monsoon storage")
        tips.append("Install efficient drip irrigation to reduce water wastage")
    elif irrigation_required > 200:
        tips.append("Moderate water requirement - Schedule irrigations carefully")
        tips.append("Mulching can reduce water loss by 30-40%")
    else:
        tips.append("Low water requirement crop - Excellent for water-scarce regions")
        tips.append("Rainfed farming possible with soil moisture conservation")
    
    # Based on soil type
    soil = input_data.soil_type
    if soil == "Sandy Loam" or soil == "Sandy":
        tips.append(f"{soil} soil drains quickly - shorter, frequent irrigations recommended")
        tips.append("Apply mulch to reduce soil moisture evaporation")
    elif soil == "Clay" or soil == "Black Soil":
        tips.append(f"{soil} soil retains water - irrigate at longer intervals")
        tips.append("Ensure good drainage to prevent waterlogging")
    
    # General tips
    tips.append("Irrigate early morning (4-7 AM) to minimize evaporation")
    tips.append("Check soil moisture 15-20 cm deep before irrigating")
    tips.append("Use drip irrigation for 30-50% water savings compared to flood")
    tips.append(f"Target {irrigation_required:.0f}mm additional water from irrigation")
    
    # Budget consideration
    if input_data.budget_inr < 30000:
        tips.append("Budget-friendly: Consider flood/furrow irrigation over drip system")
    else:
        tips.append("Budget allows for drip irrigation - long-term cost-effective solution")
    
    return tips


def calculate_irrigation_cost(method: str, schedule: List[Dict], input_data: AnalysisInput) -> float:
    """Calculate estimated irrigation cost per acre"""
    
    # Cost factors
    base_costs = {
        "Flood Irrigation (Basin Method)": 2000,
        "Flood Irrigation (Furrow Method)": 2500,
        "Sprinkler Irrigation": 4500,
        "Drip Irrigation": 5500,
        "Drip Irrigation (Micro-sprinklers)": 5000,
        "Drip Irrigation with Micro-sprinklers": 5200,
        "Drip Irrigation (Booth or Lateral Move)": 4800,
        "Sprinkler Irrigation (Boom or Lateral Move)": 4800,
        "Micro-sprinkler or Subsurface Drip": 5800,
        "Drip Irrigation (Primary) + Drip Lines with Mulch": 6500,
        "Drip Irrigation (Widely spaced crops)": 5000,
        "Mulched Field": 3000
    }
    
    # Get base cost for method or default
    base_cost = base_costs.get(method, 4000)
    
    # Calculate number of irrigations from schedule
    num_irrigations = len(schedule)
    
    # Cost per irrigation (labor, electricity, maintenance)
    cost_per_irrigation = 800 if "Drip" in method else 600
    
    # Total irrigation cost
    total_cost = base_cost + (cost_per_irrigation * num_irrigations)
    
    # Add seasonal maintenance (10% of total)
    total_cost = total_cost * 1.10
    
    # Consider land area
    land_area = input_data.land_area_acres
    per_acre_cost = total_cost / land_area if land_area > 0 else total_cost
    
    return round(per_acre_cost, 2)


def calculate_irrigation_efficiency(method: str) -> float:
    """Return water use efficiency percentage for irrigation method"""
    
    efficiency_map = {
        "Flood Irrigation": 40,
        "Furrow Irrigation": 50,
        "Sprinkler Irrigation": 70,
        "Drip Irrigation": 90,
        "Micro-sprinkler": 85,
        "Subsurface Drip": 92,
        "Mulched Field": 75
    }
    
    # Try to match the method
    for key, value in efficiency_map.items():
        if key.lower() in method.lower():
            return value
    
    return 60  # Default efficiency


def get_default_irrigation() -> Dict:
    """Return default irrigation plan when crop not found"""
    return {
        "irrigation_required_mm": 600,
        "total_water_needed_mm": 900,
        "rainfall_mm": 300,
        "irrigation_method": "Sprinkler Irrigation",
        "irrigation_schedule": get_default_schedule(),
        "water_management_tips": [
            "Assess your water source reliability before farming",
            "Maintain consistent soil moisture during growing season",
            "Irrigate during cool parts of the day to minimize evaporation",
            "Use mulch to conserve soil moisture",
            "Install proper drainage to prevent waterlogging"
        ],
        "estimated_cost_per_acre": 4000,
        "efficiency_percentage": 70
    }
