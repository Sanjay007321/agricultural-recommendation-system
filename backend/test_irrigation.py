import sys
sys.path.append('.')

from app.services.irrigation_service import get_irrigation_planning
from app.models.schemas import AnalysisInput

# Test different crops with different conditions
test_cases = [
    {
        "crop": "Rice",
        "input": AnalysisInput(
            land_area_acres=5,
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
            budget_inr=50000
        )
    },
    {
        "crop": "Cotton",
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
            rainfall_mm=800,
            temperature_c=32,
            humidity_percent=50,
            budget_inr=100000
        )
    },
    {
        "crop": "Groundnut",
        "input": AnalysisInput(
            land_area_acres=3,
            soil_type="Sandy Loam",
            soil_ph=6.5,
            nitrogen=20,
            phosphorus=60,
            potassium=40,
            state="Gujarat",
            district="Dahod",
            season="Kharif",
            rainfall_mm=500,
            temperature_c=30,
            humidity_percent=45,
            budget_inr=25000
        )
    }
]

print("=" * 80)
print("IRRIGATION PLANNING TEST")
print("=" * 80)

for test in test_cases:
    print(f"\n{'CROP: ' + test['crop']}")
    print("-" * 80)
    
    irrigation = get_irrigation_planning(test['crop'], test['input'])
    
    print(f"Irrigation Required:        {irrigation['irrigation_required_mm']:.1f} mm")
    print(f"Total Water Needed:         {irrigation['total_water_needed_mm']:.1f} mm")
    print(f"Rainfall:                   {irrigation['rainfall_mm']:.1f} mm")
    print(f"Irrigation Method:          {irrigation['irrigation_method']}")
    print(f"Efficiency:                 {irrigation['efficiency_percentage']}%")
    print(f"Estimated Cost/Acre:        ₹{irrigation['estimated_cost_per_acre']:.2f}")
    
    print(f"\nIrrigation Schedule ({len(irrigation['irrigation_schedule'])} stages):")
    for i, stage in enumerate(irrigation['irrigation_schedule'], 1):
        print(f"  {i}. {stage['stage']}")
        print(f"     Days: {stage['days_after_sowing']} | Depth: {stage['depth_mm']}mm")
        print(f"     Frequency: {stage['frequency']} | {stage['notes']}")
    
    print(f"\nWater Management Tips:")
    for i, tip in enumerate(irrigation['water_management_tips'], 1):
        print(f"  {i}. {tip}")
    
    print()

print("=" * 80)
print("✓ All irrigation planning tests completed successfully!")
print("=" * 80)
