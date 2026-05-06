"""
Generate sample datasets for ML model training
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "../data")
os.makedirs(OUTPUT_DIR, exist_ok=True)

def generate_crop_prices(num_days=365*3):
    """Generate synthetic crop price data for multiple crops"""
    crops = ["Rice", "Wheat", "Maize", "Soybean", "Cotton", "Sugarcane", 
             "Groundnut", "Mustard", "Chickpea", "Potato", "Onion", "Tomato"]
    
    base_prices = {
        "Rice": 2200, "Wheat": 2300, "Maize": 1900, "Soybean": 4200,
        "Cotton": 6500, "Sugarcane": 350, "Groundnut": 5500, "Mustard": 5200,
        "Chickpea": 5000, "Potato": 1200, "Onion": 1500, "Tomato": 1000
    }
    
    data = []
    np.random.seed(42)
    
    start_date = datetime.now() - timedelta(days=num_days)
    
    for crop in crops:
        base_price = base_prices.get(crop, 2000)
        current_price = base_price * 0.85  # Start lower
        
        for day in range(num_days):
            date = start_date + timedelta(days=day)
            
            # Seasonal variation
            month = date.month
            if crop in ["Rice", "Soybean", "Cotton"]:  # Kharif
                if month in [10, 11, 12]:  # Post harvest - lower prices
                    seasonal_factor = 0.92
                elif month in [6, 7, 8]:  # Pre harvest - higher prices
                    seasonal_factor = 1.08
                else:
                    seasonal_factor = 1.0
            elif crop in ["Wheat", "Mustard", "Chickpea"]:  # Rabi
                if month in [3, 4, 5]:  # Post harvest
                    seasonal_factor = 0.93
                elif month in [11, 12, 1]:  # Pre harvest
                    seasonal_factor = 1.07
                else:
                    seasonal_factor = 1.0
            else:
                seasonal_factor = 1.0
            
            # Random daily variation
            daily_change = np.random.uniform(-0.015, 0.018)
            current_price = current_price * (1 + daily_change) * (0.99 + seasonal_factor * 0.01)
            
            # Keep within reasonable bounds
            current_price = max(base_price * 0.7, min(current_price, base_price * 1.4))
            
            data.append({
                "date": date.strftime("%Y-%m-%d"),
                "crop": crop,
                "price_per_quintal": round(current_price, 2),
                "mandi": "Delhi",
                "state": "Delhi"
            })
    
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(OUTPUT_DIR, "crop_prices.csv"), index=False)
    print(f"Generated crop_prices.csv with {len(df)} records")
    return df

def generate_crop_yields():
    """Generate synthetic crop yield data"""
    crops = ["Rice", "Wheat", "Maize", "Soybean", "Cotton", "Sugarcane", 
             "Groundnut", "Mustard", "Chickpea", "Potato", "Onion", "Tomato"]
    
    base_yields = {
        "Rice": 20, "Wheat": 18, "Maize": 25, "Soybean": 12,
        "Cotton": 8, "Sugarcane": 350, "Groundnut": 10, "Mustard": 8,
        "Chickpea": 8, "Potato": 100, "Onion": 80, "Tomato": 120
    }
    
    soil_types = ["Alluvial", "Black Soil", "Red Soil", "Sandy Loam", "Loamy", "Clay"]
    seasons = ["Kharif", "Rabi", "Zaid"]
    states = ["Maharashtra", "Karnataka", "Punjab", "Uttar Pradesh", "Gujarat", "Madhya Pradesh"]
    
    data = []
    np.random.seed(123)
    
    for _ in range(5000):
        crop = np.random.choice(crops)
        base_yield = base_yields.get(crop, 15)
        
        soil = np.random.choice(soil_types)
        season = np.random.choice(seasons)
        state = np.random.choice(states)
        
        # Generate conditions
        rainfall = np.random.uniform(300, 2000)
        temperature = np.random.uniform(15, 38)
        ph = np.random.uniform(5.0, 8.5)
        nitrogen = np.random.uniform(50, 300)
        phosphorus = np.random.uniform(20, 100)
        potassium = np.random.uniform(50, 250)
        land_area = np.random.uniform(1, 20)
        
        # Calculate yield factor based on conditions
        yield_factor = 1.0
        
        # Soil factor
        if soil in ["Loamy", "Alluvial"]:
            yield_factor *= 1.1
        elif soil in ["Sandy Loam"]:
            yield_factor *= 0.95
        
        # pH factor
        if 6.0 <= ph <= 7.5:
            yield_factor *= 1.05
        elif ph < 5.5 or ph > 8.0:
            yield_factor *= 0.85
        
        # Rainfall factor
        if 600 <= rainfall <= 1500:
            yield_factor *= 1.05
        elif rainfall < 400 or rainfall > 2000:
            yield_factor *= 0.8
        
        # NPK factor
        npk_score = (nitrogen/200 + phosphorus/80 + potassium/200) / 3
        yield_factor *= (0.8 + 0.4 * min(npk_score, 1.0))
        
        # Random variation
        yield_factor *= np.random.uniform(0.85, 1.15)
        
        actual_yield = base_yield * yield_factor
        total_yield = actual_yield * land_area
        
        data.append({
            "crop": crop,
            "state": state,
            "season": season,
            "soil_type": soil,
            "rainfall_mm": round(rainfall, 1),
            "temperature_c": round(temperature, 1),
            "ph": round(ph, 1),
            "nitrogen": round(nitrogen, 1),
            "phosphorus": round(phosphorus, 1),
            "potassium": round(potassium, 1),
            "land_area_acres": round(land_area, 1),
            "yield_per_acre": round(actual_yield, 2),
            "total_yield": round(total_yield, 2)
        })
    
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(OUTPUT_DIR, "crop_yields.csv"), index=False)
    print(f"Generated crop_yields.csv with {len(df)} records")
    return df

def generate_soil_crop_data():
    """Generate soil-crop suitability data for classification"""
    crops = ["Rice", "Wheat", "Maize", "Soybean", "Cotton", "Sugarcane", 
             "Groundnut", "Mustard", "Chickpea", "Potato", "Onion", "Tomato"]
    
    soil_types = ["Alluvial", "Black Soil", "Red Soil", "Sandy Loam", "Loamy", "Clay", "Clay Loam"]
    seasons = ["Kharif", "Rabi", "Zaid"]
    
    # Crop preferences
    crop_soil_prefs = {
        "Rice": ["Clay", "Loamy", "Alluvial"],
        "Wheat": ["Loamy", "Clay Loam", "Alluvial"],
        "Maize": ["Loamy", "Sandy Loam", "Alluvial"],
        "Soybean": ["Black Soil", "Loamy", "Clay Loam"],
        "Cotton": ["Black Soil", "Alluvial", "Red Soil"],
        "Sugarcane": ["Loamy", "Clay Loam", "Alluvial"],
        "Groundnut": ["Sandy Loam", "Red Soil", "Loamy"],
        "Mustard": ["Loamy", "Sandy Loam", "Alluvial"],
        "Chickpea": ["Loamy", "Clay Loam", "Black Soil"],
        "Potato": ["Sandy Loam", "Loamy", "Alluvial"],
        "Onion": ["Loamy", "Sandy Loam", "Clay Loam"],
        "Tomato": ["Loamy", "Sandy Loam", "Clay Loam"]
    }
    
    data = []
    np.random.seed(456)
    
    for _ in range(10000):
        soil = np.random.choice(soil_types)
        season = np.random.choice(seasons)
        
        rainfall = np.random.uniform(200, 2500)
        temperature = np.random.uniform(10, 40)
        ph = np.random.uniform(4.5, 9.0)
        nitrogen = np.random.uniform(30, 350)
        phosphorus = np.random.uniform(10, 120)
        potassium = np.random.uniform(30, 300)
        
        # Determine best crop based on conditions
        scores = {}
        for crop in crops:
            score = 0
            
            # Soil match
            if soil in crop_soil_prefs.get(crop, []):
                score += 30
            
            # Season match (simplified)
            if crop in ["Rice", "Maize", "Soybean", "Cotton", "Groundnut"] and season == "Kharif":
                score += 20
            elif crop in ["Wheat", "Mustard", "Chickpea", "Potato"] and season == "Rabi":
                score += 20
            elif crop in ["Tomato", "Onion"] and season in ["Rabi", "Zaid"]:
                score += 15
            
            # Temperature (simplified)
            if 20 <= temperature <= 32:
                score += 10
            
            # pH (simplified)
            if 6.0 <= ph <= 7.5:
                score += 10
            
            # Add some randomness
            score += np.random.uniform(-5, 5)
            scores[crop] = score
        
        best_crop = max(scores, key=scores.get)
        
        data.append({
            "soil_type": soil,
            "season": season,
            "rainfall_mm": round(rainfall, 1),
            "temperature_c": round(temperature, 1),
            "ph": round(ph, 2),
            "nitrogen": round(nitrogen, 1),
            "phosphorus": round(phosphorus, 1),
            "potassium": round(potassium, 1),
            "recommended_crop": best_crop
        })
    
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(OUTPUT_DIR, "soil_crop_data.csv"), index=False)
    print(f"Generated soil_crop_data.csv with {len(df)} records")
    return df

def generate_disease_data():
    """Generate disease occurrence data"""
    crops = ["Rice", "Wheat", "Cotton", "Soybean", "Tomato", "Potato"]
    
    diseases = {
        "Rice": ["Blast", "Brown Spot", "Bacterial Leaf Blight"],
        "Wheat": ["Rust", "Loose Smut", "Powdery Mildew"],
        "Cotton": ["Bollworm", "Whitefly", "Bacterial Blight"],
        "Soybean": ["Yellow Mosaic", "Pod Borer", "Rust"],
        "Tomato": ["Early Blight", "Late Blight", "Fruit Borer"],
        "Potato": ["Late Blight", "Early Blight"]
    }
    
    data = []
    np.random.seed(789)
    
    for _ in range(3000):
        crop = np.random.choice(crops)
        
        humidity = np.random.uniform(40, 95)
        temperature = np.random.uniform(15, 38)
        rainfall = np.random.uniform(200, 2000)
        season = np.random.choice(["Kharif", "Rabi", "Zaid"])
        
        # Calculate disease risk
        risk_score = 0
        if humidity > 75:
            risk_score += 30
        elif humidity > 60:
            risk_score += 15
        
        if rainfall > 1200:
            risk_score += 25
        elif rainfall > 800:
            risk_score += 10
        
        if 22 <= temperature <= 30 and humidity > 70:
            risk_score += 20
        
        if season == "Kharif":
            risk_score += 10
        
        # Add randomness
        risk_score += np.random.uniform(-10, 10)
        
        if risk_score >= 50:
            risk_level = "High"
            disease = np.random.choice(diseases.get(crop, ["Unknown"]))
        elif risk_score >= 25:
            risk_level = "Medium"
            disease = np.random.choice(diseases.get(crop, ["Unknown"]) + ["None"])
        else:
            risk_level = "Low"
            disease = "None"
        
        data.append({
            "crop": crop,
            "season": season,
            "humidity_percent": round(humidity, 1),
            "temperature_c": round(temperature, 1),
            "rainfall_mm": round(rainfall, 1),
            "disease_risk": risk_level,
            "disease_occurred": disease
        })
    
    df = pd.DataFrame(data)
    df.to_csv(os.path.join(OUTPUT_DIR, "disease_data.csv"), index=False)
    print(f"Generated disease_data.csv with {len(df)} records")
    return df

if __name__ == "__main__":
    print("Generating sample datasets for ML training...")
    print("-" * 50)
    
    generate_crop_prices()
    generate_crop_yields()
    generate_soil_crop_data()
    generate_disease_data()
    
    print("-" * 50)
    print("All datasets generated successfully!")
