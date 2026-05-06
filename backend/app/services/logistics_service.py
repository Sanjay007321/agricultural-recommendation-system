from typing import Dict
from app.models.schemas import AnalysisInput

# Distance matrix (approximate km between major cities)
MANDI_DISTANCES = {
    "Maharashtra": {"Pune APMC": 0, "Mumbai APMC": 150, "Nashik APMC": 200, "Nagpur APMC": 700},
    "Karnataka": {"Bangalore APMC": 0, "Mysore APMC": 150, "Hubli APMC": 400},
    "Gujarat": {"Ahmedabad APMC": 0, "Surat APMC": 250, "Rajkot APMC": 220},
    "Madhya Pradesh": {"Bhopal APMC": 0, "Indore APMC": 200, "Jabalpur APMC": 300},
    "Uttar Pradesh": {"Lucknow APMC": 0, "Kanpur APMC": 80, "Varanasi APMC": 300},
    "Punjab": {"Ludhiana APMC": 0, "Amritsar APMC": 150, "Jalandhar APMC": 60},
    "Rajasthan": {"Jaipur APMC": 0, "Jodhpur APMC": 350, "Kota APMC": 250},
    "Tamil Nadu": {"Chennai APMC": 0, "Coimbatore APMC": 500, "Madurai APMC": 450},
}

# Transport rates (Rs per quintal per km)
TRANSPORT_RATES = {
    "truck": 2.5,  # For >50 quintals
    "tempo": 3.5,  # For 10-50 quintals
    "auto": 5.0    # For <10 quintals
}

# Mandi fees (typically 1-2% of value)
MANDI_FEE_PERCENT = 1.5

# Loading/unloading charges per quintal
LOADING_CHARGE_PER_QUINTAL = 15
UNLOADING_CHARGE_PER_QUINTAL = 15

def estimate_distance(state: str, mandi: str) -> float:
    """Estimate distance to mandi in km"""
    state_mandis = MANDI_DISTANCES.get(state, {})
    
    if mandi in state_mandis:
        return state_mandis[mandi]
    
    # Default distance if mandi not found
    return 50  # Assume 50 km average

def get_transport_rate(quantity_quintals: float) -> float:
    """Get transport rate based on quantity"""
    if quantity_quintals > 50:
        return TRANSPORT_RATES["truck"]
    elif quantity_quintals > 10:
        return TRANSPORT_RATES["tempo"]
    else:
        return TRANSPORT_RATES["auto"]

def calculate_logistics_cost(
    crop_name: str, 
    total_yield_quintal: float, 
    input_data: AnalysisInput
) -> Dict:
    """
    Calculate logistics cost including transport, loading, mandi fees
    """
    # Estimate distance
    mandi = input_data.nearest_mandi or f"{input_data.district} APMC"
    distance = estimate_distance(input_data.state, mandi)
    
    # Transport cost
    transport_rate = get_transport_rate(total_yield_quintal)
    transport_cost = distance * transport_rate * total_yield_quintal
    
    # Loading and unloading
    loading_cost = total_yield_quintal * LOADING_CHARGE_PER_QUINTAL
    unloading_cost = total_yield_quintal * UNLOADING_CHARGE_PER_QUINTAL
    loading_unloading = loading_cost + unloading_cost
    
    # Mandi fees (based on estimated value)
    # Using average price of Rs 3000/quintal for estimation
    estimated_value = total_yield_quintal * 3000
    mandi_fees = estimated_value * (MANDI_FEE_PERCENT / 100)
    
    # Storage cost (if needed - assume 0 for direct sale)
    storage_cost = 0
    
    total_logistics = transport_cost + loading_unloading + mandi_fees + storage_cost
    
    return {
        "transport_to_mandi": round(transport_cost, 0),
        "loading_unloading": round(loading_unloading, 0),
        "mandi_fees": round(mandi_fees, 0),
        "storage_if_needed": round(storage_cost, 0),
        "total_logistics": round(total_logistics, 0),
        "distance_km": distance,
        "transport_rate": transport_rate
    }
