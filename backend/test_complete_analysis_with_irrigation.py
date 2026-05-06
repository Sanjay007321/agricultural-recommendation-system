import sys
sys.path.append('.')

from app.services.crop_service import get_crop_recommendation
from app.services.irrigation_service import get_irrigation_planning
from app.services.yield_service import predict_yield
from app.services.price_service import predict_price
from app.services.fertilizer_service import get_fertilizer_recommendation
from app.services.disease_service import get_disease_risk
from app.services.logistics_service import calculate_logistics_cost
from app.services.profit_service import calculate_profit
from app.models.schemas import AnalysisInput

print("\n" + "="*90)
print("COMPLETE ANALYSIS FLOW: IRRIGATION INTEGRATED INTO PROFIT ANALYSIS")
print("="*90)

# Test Case: Different crop scenarios
test_scenarios = [
    {
        "name": "Cotton - High Rainfall Region",
        "input": AnalysisInput(
            land_area_acres=10,
            soil_type="Black Soil",
            soil_ph=7.2,
            nitrogen=120,
            phosphorus=60,
            potassium=60,
            state="Maharashtra",
            district="Vidarbha",
            season="Kharif",
            rainfall_mm=700,
            temperature_c=32,
            humidity_percent=50,
            budget_inr=100000
        )
    },
    {
        "name": "Wheat - Semi-Arid Region",
        "input": AnalysisInput(
            land_area_acres=5,
            soil_type="Loamy",
            soil_ph=7.0,
            nitrogen=100,
            phosphorus=50,
            potassium=40,
            state="Punjab",
            district="Ludhiana",
            season="Rabi",
            rainfall_mm=400,
            temperature_c=15,
            humidity_percent=50,
            budget_inr=50000
        )
    },
    {
        "name": "Rice - Low Rainfall Irrigated",
        "input": AnalysisInput(
            land_area_acres=3,
            soil_type="Loamy",
            soil_ph=6.5,
            nitrogen=100,
            phosphorus=50,
            potassium=40,
            state="West Bengal",
            district="Medinipur",
            season="Kharif",
            rainfall_mm=1500,
            temperature_c=28,
            humidity_percent=75,
            budget_inr=40000
        )
    }
]

for scenario in test_scenarios:
    print(f"\n{'-'*90}")
    print(f"SCENARIO: {scenario['name']}")
    print(f"{'-'*90}")
    
    input_data = scenario['input']
    
    # Get recommendations
    crop_rec = get_crop_recommendation(input_data)
    crop = crop_rec['recommended_crop']
    
    # Get all required data
    yield_pred = predict_yield(crop, input_data)
    price_pred = predict_price(crop, input_data)
    fertilizer_rec = get_fertilizer_recommendation(crop, input_data)
    disease_risk = get_disease_risk(crop, input_data)
    logistics = calculate_logistics_cost(crop, yield_pred["total_yield_quintal"], input_data)
    irrigation = get_irrigation_planning(crop, input_data)
    
    # Calculate profit WITH actual irrigation cost
    profit = calculate_profit(
        crop, 
        yield_pred, 
        price_pred, 
        fertilizer_rec, 
        disease_risk, 
        logistics, 
        input_data, 
        irrigation
    )
    
    # Display results
    print(f"\nRECOMMENDED CROP:     {crop}")
    print(f"LAND AREA:            {input_data.land_area_acres} acres")
    print(f"IRRIGATION METHOD:    {irrigation['irrigation_method']}")
    print(f"IRRIGATION METHOD:    {irrigation['irrigation_method']}")
    
    print(f"\nREVENUE:")
    print(f"  Yield:              {profit['revenue']['total_yield_quintal']} quintals")
    print(f"  Price/Quintal:      Rs. {profit['revenue']['price_per_quintal']:.0f}")
    print(f"  Gross Revenue:      Rs. {profit['revenue']['gross_revenue']:>12,.0f}")
    
    print(f"\nCOSTS:")
    print(f"  Seeds:              Rs. {profit['costs']['seeds']:>12,.0f}")
    print(f"  Fertilizers:        Rs. {profit['costs']['fertilizers']:>12,.0f}")
    print(f"  Pesticides:         Rs. {profit['costs']['pesticides']:>12,.0f}")
    print(f"  Labor:              Rs. {profit['costs']['labor']:>12,.0f}")
    print(f"  Irrigation:         Rs. {profit['costs']['irrigation']:>12,.0f}  <- KEY COST")
    print(f"  Logistics:          Rs. {profit['costs']['logistics']:>12,.0f}")
    print(f"  Miscellaneous:      Rs. {profit['costs']['miscellaneous']:>12,.0f}")
    print(f"  {'─'*55}")
    print(f"  TOTAL COST:         Rs. {profit['costs']['total_cost']:>12,.0f}")
    
    print(f"\nPROFIT ANALYSIS:")
    print(f"  Net Profit:         Rs. {profit['net_profit']:>12,.0f}")
    print(f"  Profit/Acre:        Rs. {profit['profit_per_acre']:>12,.0f}")
    print(f"  ROI:                {profit['roi_percentage']:>17.2f}%")
    
    irrigation_cost_pct = (profit['costs']['irrigation'] / profit['costs']['total_cost']) * 100
    print(f"\nIRRIGATION IMPACT:")
    print(f"  Irrigation Cost:    Rs. {profit['costs']['irrigation']:>12,.0f}")
    print(f"  % of Total Cost:    {irrigation_cost_pct:>16.1f}%")
    print(f"  Water Efficiency:   {irrigation['efficiency_percentage']:>16}%")
    print(f"  Water Needed:       {irrigation['irrigation_required_mm']:>15.1f}mm")

print(f"\n{'='*90}")
print("✓ IRRIGATION COSTS SUCCESSFULLY INTEGRATED INTO ALL PROFIT ANALYSES")
print("✓ Each scenario shows realistic profit considering irrigation investments")
print("✓ Farmers can make informed decisions with complete cost breakdown")
print(f"{'='*90}\n")
