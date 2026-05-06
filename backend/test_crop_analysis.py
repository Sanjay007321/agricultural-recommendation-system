#!/usr/bin/env python
import sys
from app.models.schemas import AnalysisInput
from app.services.crop_service import get_crop_recommendation

# Create a test input
input_data = AnalysisInput(
    land_area_acres=2.0,
    soil_type="Loamy",
    soil_ph=6.5,
    nitrogen=150,
    phosphorus=50,
    potassium=100,
    state="Tamil Nadu",
    district="Coimbatore",
    season="Kharif(June to October)",
    rainfall_mm=800,
    temperature_c=28,
    humidity_percent=60,
    budget_inr=100000,
    crop_preference="auto"
)

# Test the recommendation
try:
    result = get_crop_recommendation(input_data)
    print("✓ Success! Recommendation result:")
    print(f"Keys in result: {list(result.keys())}")
    print(f"Recommended crop: {result.get('recommended_crop')}")
    print(f"Suitable lands: {result.get('suitable_lands')}")
    print(f"Confidence: {result.get('confidence')}")
    print(f"Recommended variety: {result.get('recommended_variety')}")
except Exception as e:
    print(f"✗ Error: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
