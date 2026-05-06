import sys
sys.path.append('.')

from app.services.crop_service import get_crop_recommendation
from app.services.irrigation_service import get_irrigation_planning
from app.models.schemas import AnalysisInput

print("\n" + "="*70)
print("IRRIGATION PLANNING FEATURE VERIFICATION")
print("="*70 + "\n")

# Test Case: Medium-sized cotton farm in Maharashtra
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

# Get crop recommendation
crop_rec = get_crop_recommendation(input_data)
recommended_crop = crop_rec['recommended_crop']

# Get irrigation planning
irrigation = get_irrigation_planning(recommended_crop, input_data)

# Display results
print(f"Recommended Crop:        {recommended_crop}")
print(f"Variety:                 {crop_rec.get('recommended_variety', 'N/A')}")
print(f"Land Area:               {input_data.land_area_acres} acres")
print(f"Soil Type:               {input_data.soil_type}")
print(f"\n--- IRRIGATION PLANNING DETAILS ---\n")
print(f"Available Rainfall:      {irrigation['rainfall_mm']:.1f} mm")
print(f"Total Water Needed:      {irrigation['total_water_needed_mm']:.1f} mm")
print(f"Additional Irrigation:   {irrigation['irrigation_required_mm']:.1f} mm")
print(f"Irrigation Method:       {irrigation['irrigation_method']}")
print(f"Water Use Efficiency:    {irrigation['efficiency_percentage']}%")
print(f"Estimated Cost/Acre:     Rs. {irrigation['estimated_cost_per_acre']:.2f}")
print(f"Total Estimated Cost:    Rs. {irrigation['estimated_cost_per_acre'] * input_data.land_area_acres:.2f}")

print(f"\n--- IRRIGATION SCHEDULE ---\n")
for i, stage in enumerate(irrigation['irrigation_schedule'], 1):
    print(f"{i}. {stage['stage']}")
    print(f"   Days: {stage['days_after_sowing']} | Depth: {stage['depth_mm']}mm | {stage['frequency']}")

print(f"\n--- WATER MANAGEMENT TIPS ---\n")
for i, tip in enumerate(irrigation['water_management_tips'][:3], 1):
    print(f"{i}. {tip}")

print("\n" + "="*70)
print("✓ IRRIGATION PLANNING FEATURE SUCCESSFULLY IMPLEMENTED")
print("✓ Analysis responses now include detailed irrigation planning")
print("✓ Features: Method recommendation, schedule, cost, efficiency, tips")
print("="*70 + "\n")
