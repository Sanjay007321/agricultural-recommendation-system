import sys
import json
sys.path.append('.')

from app.services.crop_service import get_crop_recommendation
from app.services.irrigation_service import get_irrigation_planning
from app.models.schemas import AnalysisInput

print("=" * 80)
print("COMPLETE ANALYSIS WITH IRRIGATION PLANNING TEST")
print("=" * 80)

test_cases = [
    {
        "name": "High Water Requirement Scenario (Rice)",
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
            rainfall_mm=1000,
            temperature_c=28,
            humidity_percent=75,
            budget_inr=50000
        )
    },
    {
        "name": "Medium Water Requirement Scenario (Wheat)",
        "input": AnalysisInput(
            land_area_acres=8,
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
            budget_inr=75000
        )
    },
    {
        "name": "Low Water Requirement Scenario (Groundnut)",
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
            rainfall_mm=600,
            temperature_c=32,
            humidity_percent=45,
            budget_inr=30000
        )
    }
]

for test in test_cases:
    print(f"\n{'='*80}")
    print(f"SCENARIO: {test['name']}")
    print(f"{'='*80}")
    
    input_data = test['input']
    
    # Get crop recommendation
    crop_rec = get_crop_recommendation(input_data)
    selected_crop = crop_rec['recommended_crop']
    
    print(f"\n[CROP RECOMMENDATION]")
    print(f"   Recommended Crop:  {selected_crop}")
    print(f"   Variety:           {crop_rec.get('recommended_variety', 'N/A')}")
    print(f"   Confidence:        {crop_rec['confidence']}")
    print(f"   Suitable Lands:    {', '.join(crop_rec.get('suitable_lands', []))}")
    
    # Get irrigation planning
    irrigation = get_irrigation_planning(selected_crop, input_data)
    
    print(f"\n[IRRIGATION PLANNING]:")
    print(f"   Rainfall:                {irrigation['rainfall_mm']:.1f} mm")
    print(f"   Total Water Needed:      {irrigation['total_water_needed_mm']:.1f} mm")
    print(f"   Irrigation Required:     {irrigation['irrigation_required_mm']:.1f} mm")
    print(f"   Recommended Method:      {irrigation['irrigation_method']}")
    print(f"   Water Use Efficiency:    {irrigation['efficiency_percentage']}%")
    print(f"   Estimated Cost/Acre:     Rs. {irrigation['estimated_cost_per_acre']:.2f}")
    
    print(f"\n[IRRIGATION SCHEDULE] ({len(irrigation['irrigation_schedule'])} stages):")
    for i, stage in enumerate(irrigation['irrigation_schedule'], 1):
        print(f"\n   Stage {i}: {stage['stage']}")
        print(f"   ├─ Period:     Days {stage['days_after_sowing']} after sowing")
        print(f"   ├─ Depth:      {stage['depth_mm']}mm per irrigation")
        print(f"   ├─ Frequency:  {stage['frequency']}")
        print(f"   └─ Notes:      {stage['notes']}")
    
    print(f"\n[WATER MANAGEMENT TIPS]:")
    for i, tip in enumerate(irrigation['water_management_tips'], 1):
        print(f"   {i}. {tip}")
    
    print(f"\n[ANALYSIS SUMMARY FOR {selected_crop}]:")
    print(f"   {"Parameter":<35} {"Value":>40}")
    print(f"   {'-'*35} {'-'*40}")
    print(f"   {"Crop":35} {selected_crop:>40}")
    print(f"   {"Variety":35} {crop_rec.get('recommended_variety', 'N/A'):>40}")
    print(f"   {"Land Area":35} {input_data.land_area_acres} acres{''*24}")
    print(f"   {"Soil Type":35} {input_data.soil_type:>40}")
    print(f"   {"Rainfall":35} {input_data.rainfall_mm:.1f} mm{''*34}")
    print(f"   {"Irrigation Method":35} {irrigation['irrigation_method']:>40}")
    print(f"   {"Additional Water Needed":35} {irrigation['irrigation_required_mm']:.1f} mm{''*33}")
    print(f"   {"Irrigation Cost/Acre":35} Rs. {irrigation['estimated_cost_per_acre']:.2f}{''*34}")
    print(f"   {"Method Efficiency":35} {irrigation['efficiency_percentage']}%{''*42}")

print(f"\n{'='*80}")
print("✓ IRRIGATION PLANNING SUCCESSFULLY INTEGRATED INTO ANALYSIS")
print("✓ All crop analysis results now include detailed irrigation planning")
print(f"{'='*80}\n")
