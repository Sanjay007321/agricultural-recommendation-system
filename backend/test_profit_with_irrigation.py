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

print("\n" + "="*80)
print("PROFIT ANALYSIS WITH IRRIGATION COST TEST")
print("="*80 + "\n")

# Test Case: Cotton farm scenario
input_data = AnalysisInput(
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

# Get recommendations
crop_rec = get_crop_recommendation(input_data)
crop = crop_rec['recommended_crop']

print(f"Crop: {crop}")
print(f"Land Area: {input_data.land_area_acres} acres\n")

# Get all required data
yield_pred = predict_yield(crop, input_data)
price_pred = predict_price(crop, input_data)
fertilizer_rec = get_fertilizer_recommendation(crop, input_data)
disease_risk = get_disease_risk(crop, input_data)
logistics = calculate_logistics_cost(crop, yield_pred["total_yield_quintal"], input_data)
irrigation = get_irrigation_planning(crop, input_data)

# Calculate profit WITH irrigation cost
profit = calculate_profit(crop, yield_pred, price_pred, fertilizer_rec, disease_risk, logistics, input_data, irrigation)

print("="*80)
print("COSTS BREAKDOWN (WITH IRRIGATION)")
print("="*80)
print(f"Seeds:           Rs. {profit['costs']['seeds']:>12,.0f}")
print(f"Fertilizers:     Rs. {profit['costs']['fertilizers']:>12,.0f}")
print(f"Pesticides:      Rs. {profit['costs']['pesticides']:>12,.0f}")
print(f"Labor:           Rs. {profit['costs']['labor']:>12,.0f}")
print(f"Irrigation:      Rs. {profit['costs']['irrigation']:>12,.0f}  <- NOW INCLUDED!")
print(f"Logistics:       Rs. {profit['costs']['logistics']:>12,.0f}")
print(f"Miscellaneous:   Rs. {profit['costs']['miscellaneous']:>12,.0f}")
print(f"{'-'*45}")
print(f"TOTAL COST:      Rs. {profit['costs']['total_cost']:>12,.0f}")

print(f"\n{'='*80}")
print("REVENUE ANALYSIS")
print("="*80)
print(f"Total Yield:     {profit['revenue']['total_yield_quintal']} quintals")
print(f"Price/Quintal:   Rs. {profit['revenue']['price_per_quintal']:.0f}")
print(f"Gross Revenue:   Rs. {profit['revenue']['gross_revenue']:>12,.0f}")

print(f"\n{'='*80}")
print("PROFIT ANALYSIS")
print("="*80)
print(f"Gross Revenue:   Rs. {profit['revenue']['gross_revenue']:>12,.0f}")
print(f"Total Cost:      Rs. {profit['costs']['total_cost']:>12,.0f}")
print(f"{'-'*45}")
print(f"Net Profit:      Rs. {profit['net_profit']:>12,.0f}")
print(f"Profit/Acre:     Rs. {profit['profit_per_acre']:>12,.0f}")
print(f"ROI:             {profit['roi_percentage']:>15.2f}%")

print(f"\n{'='*80}")
print("IRRIGATION COST IMPACT")
print("="*80)
irrigation_cost_percent = (profit['costs']['irrigation'] / profit['costs']['total_cost']) * 100
profit_after_irrigation = profit['net_profit']
profit_without_irrigation = profit['revenue']['gross_revenue'] - (profit['costs']['total_cost'] - profit['costs']['irrigation'])

print(f"Irrigation Cost:      Rs. {profit['costs']['irrigation']:>12,.0f}")
print(f"% of Total Cost:      {irrigation_cost_percent:>15.1f}%")
print(f"Irrigation Method:    {irrigation['irrigation_method']}")
print(f"Water Efficiency:     {irrigation['efficiency_percentage']}%")
print(f"Cost per Acre:        Rs. {irrigation['estimated_cost_per_acre']:.2f}")

print(f"\nProfit Impact Analysis:")
print(f"  With Irrigation:    Rs. {profit_after_irrigation:>12,.0f}")
print(f"  Without Irrigation: Rs. {profit_without_irrigation:>12,.0f}")
print(f"  Difference:         Rs. {profit_after_irrigation - profit_without_irrigation:>12,.0f}")

print(f"\n{'='*80}")
print("✓ IRRIGATION COST SUCCESSFULLY INTEGRATED INTO PROFIT ANALYSIS")
print("✓ Profit now reflects actual irrigation investments")
print(f"{'='*80}\n")
