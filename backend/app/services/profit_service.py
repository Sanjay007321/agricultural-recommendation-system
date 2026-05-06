import json
import os
from typing import Dict
from app.models.schemas import AnalysisInput

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")

def load_crops_data():
    with open(os.path.join(DATA_PATH, "crops.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def get_crop_info(crop_name: str) -> Dict:
    crops_data = load_crops_data()
    for crop in crops_data.get("crops", []):
        if crop["name"].lower() == crop_name.lower():
            return crop
    return None

def calculate_profit(
    crop_name: str,
    yield_pred: Dict,
    price_pred: Dict,
    fertilizer_rec: Dict,
    disease_risk: Dict,
    logistics: Dict,
    input_data: AnalysisInput,
    irrigation: Dict = None
) -> Dict:
    """
    Calculate comprehensive profit analysis including actual irrigation costs
    """
    crop = get_crop_info(crop_name)
    land_area = input_data.land_area_acres
    
    # ============ REVENUE ============
    total_yield = yield_pred["total_yield_quintal"]
    price_per_quintal = price_pred["predicted_price"]
    gross_revenue = total_yield * price_per_quintal
    
    revenue = {
        "total_yield_quintal": total_yield,
        "price_per_quintal": price_per_quintal,
        "gross_revenue": round(gross_revenue, 0)
    }
    
    # ============ COSTS ============
    
    # Seed cost
    if crop:
        seed_cost = crop.get("seed_cost_per_acre", 1500) * land_area
    else:
        seed_cost = 1500 * land_area
    
    # Fertilizer cost (from recommendation)
    fertilizer_cost = fertilizer_rec.get("total_cost", 5000)
    
    # Pesticide cost (from disease risk analysis)
    pesticide_cost = disease_risk.get("total_cost", 2000)
    
    # Labor cost
    if crop:
        labor_cost = crop.get("labor_cost_per_acre", 6000) * land_area
    else:
        labor_cost = 6000 * land_area
    
    # Irrigation cost (from irrigation planning service)
    if irrigation:
        irrigation_cost = irrigation.get("estimated_cost_per_acre", 2000) * land_area
    else:
        # Fallback estimation if irrigation data not provided
        if input_data.rainfall_mm < 600:
            irrigation_cost = 3000 * land_area  # High irrigation need
        elif input_data.rainfall_mm < 1000:
            irrigation_cost = 1500 * land_area  # Medium irrigation
        else:
            irrigation_cost = 500 * land_area   # Low irrigation need
    
    # Logistics cost (from logistics service)
    logistics_cost = logistics.get("total_logistics", 5000)
    
    # Miscellaneous (5% of other costs)
    other_costs = seed_cost + fertilizer_cost + pesticide_cost + labor_cost + irrigation_cost
    miscellaneous = other_costs * 0.05
    
    # Total cost
    total_cost = (seed_cost + fertilizer_cost + pesticide_cost + 
                  labor_cost + irrigation_cost + logistics_cost + miscellaneous)
    
    costs = {
        "seeds": round(seed_cost, 0),
        "fertilizers": round(fertilizer_cost, 0),
        "pesticides": round(pesticide_cost, 0),
        "labor": round(labor_cost, 0),
        "irrigation": round(irrigation_cost, 0),
        "logistics": round(logistics_cost, 0),
        "miscellaneous": round(miscellaneous, 0),
        "total_cost": round(total_cost, 0)
    }
    
    # ============ PROFIT ============
    net_profit = gross_revenue - total_cost
    profit_per_acre = net_profit / land_area if land_area > 0 else 0
    roi_percentage = (net_profit / total_cost * 100) if total_cost > 0 else 0
    
    # ============ COMPARISON WITH ALTERNATIVES ============
    # Calculate estimated profit for alternative crops
    comparisons = []
    crops_data = load_crops_data()
    
    # Get top 3 alternative crops by potential profit
    for alt_crop in crops_data.get("crops", [])[:5]:
        if alt_crop["name"].lower() != crop_name.lower():
            alt_yield = alt_crop.get("avg_yield_quintal_per_acre", 10) * land_area * 0.9
            alt_price = alt_crop.get("avg_price_per_quintal", 2000)
            alt_revenue = alt_yield * alt_price
            
            alt_seed = alt_crop.get("seed_cost_per_acre", 1500) * land_area
            alt_labor = alt_crop.get("labor_cost_per_acre", 6000) * land_area
            alt_other = (fertilizer_cost + pesticide_cost + irrigation_cost + logistics_cost) * 0.9
            alt_total_cost = alt_seed + alt_labor + alt_other
            
            alt_profit = alt_revenue - alt_total_cost
            
            comparisons.append({
                "crop": alt_crop["name"],
                "estimated_profit": round(alt_profit, 0),
                "yield": round(alt_yield, 1),
                "price": alt_price
            })
    
    # Sort by profit
    comparisons.sort(key=lambda x: x["estimated_profit"], reverse=True)
    
    return {
        "revenue": revenue,
        "costs": costs,
        "net_profit": round(net_profit, 0),
        "profit_per_acre": round(profit_per_acre, 0),
        "roi_percentage": round(roi_percentage, 1),
        "comparison_with_alternatives": comparisons[:3]
    }
