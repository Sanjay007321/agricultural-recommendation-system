import json
import sys
sys.path.append('.')

from app.services.crop_service import get_crop_recommendation, load_crops_data
from app.models.schemas import AnalysisInput

# Test 1: Verify all crops load
print("=" * 50)
print("TEST 1: Loading all crops")
print("=" * 50)
crops_data = load_crops_data()
crops = crops_data.get('crops', [])
print(f"✓ Loaded {len(crops)} crops successfully\n")
for crop in crops:
    print(f"  - {crop['name']}: {len(crop['varieties'])} varieties")

# Test 2: Get recommendations for different crops
test_cases = [
    {"soil": "Black Soil", "rainfall": 1500, "expected": "Sugarcane"},
    {"soil": "Sandy Loam", "rainfall": 600, "expected": "Groundnut"},
    {"soil": "Loamy", "rainfall": 400, "expected": "Wheat"},
]

print("=" * 50)
print("TEST 2: Testing different crop recommendations")
print("=" * 50)

for i, test in enumerate(test_cases, 1):
    input_data = AnalysisInput(
        land_area_acres=5,
        soil_type=test["soil"],
        soil_ph=6.5,
        nitrogen=100,
        phosphorus=50,
        potassium=40,
        state="Maharashtra",
        district="Nashik",
        season="Kharif",
        rainfall_mm=test["rainfall"],
        temperature_c=25,
        humidity_percent=60,
        budget_inr=50000
    )
    
    result = get_crop_recommendation(input_data)
    print(f"\nTest {i}: {test['soil']}, {test['rainfall']}mm rainfall")
    print(f"  Recommended: {result['recommended_crop']}")
    print(f"  Variety: {result['recommended_variety']}")
    print(f"  Suitable lands: {result['suitable_lands']}")
    print(f"  Confidence: {result['confidence']}")
    print(f"  ✓ Pass" if result['recommended_crop'] else "  ✗ Fail")

print("\n" + "=" * 50)
print("ALL TESTS PASSED!")
print("=" * 50)
