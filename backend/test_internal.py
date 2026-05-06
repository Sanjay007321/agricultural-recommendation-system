import os
import sys

# Add backend to path
sys.path.append(r"c:\SKS\crop\backend")

from app.models.schemas import AnalysisInput
from app.models.user import User
from app.database import SessionLocal
from app.api.analysis import analyze_crop

def debug():
    db = SessionLocal()
    
    # Mock user
    user = db.query(User).filter(User.mobile == "7171717171").first()
    if not user:
        print("User not found")
        return

    input_data = AnalysisInput(
        land_area_acres=5.0,
        soil_type="Loamy",
        soil_ph=6.5,
        nitrogen=150,
        phosphorus=50,
        potassium=100,
        state="Tamil Nadu",
        district="Chennai",
        season="",
        rainfall_mm=800,
        temperature_c=28,
        humidity_percent=60,
        budget_inr=50000,
        crop_preference="auto",
        crop_variety="",
        nearest_mandi="",
        sowing_date="2026-03-20"
    )

    try:
        print("Running analyze_crop...")
        result = analyze_crop(input_data, user, db)
        print("Success:", result.analysis_id)
    except Exception as e:
        import traceback
        print("CRASH TRACEBACK:")
        traceback.print_exc()

if __name__ == "__main__":
    debug()
