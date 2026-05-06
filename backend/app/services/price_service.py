import json
import os
import numpy as np
from typing import Dict, List
from app.models.schemas import AnalysisInput

DATA_PATH = os.path.join(os.path.dirname(__file__), "../data")
MODEL_PATH = os.path.join(os.path.dirname(__file__), "../ml/models")

def load_crops_data():
    with open(os.path.join(DATA_PATH, "crops.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def get_base_price(crop_name: str) -> float:
    """Get base price for a crop from data"""
    crops_data = load_crops_data()
    for crop in crops_data.get("crops", []):
        if crop["name"].lower() == crop_name.lower():
            return crop.get("avg_price_per_quintal", 2000)
    return 2000  # Default price

def simulate_lstm_prediction(crop_name: str, input_data: AnalysisInput) -> List[float]:
    """
    Simulates LSTM price prediction
    In production, this would load a trained LSTM model
    """
    base_price = get_base_price(crop_name)
    
    # Seasonal factors
    season_factors = {
        "Kharif": {"start": 0.95, "end": 1.10},  # Price increases after harvest
        "Rabi": {"start": 0.92, "end": 1.08},
        "Zaid": {"start": 0.98, "end": 1.05}
    }
    
    season_factor = season_factors.get(input_data.season, {"start": 1.0, "end": 1.05})
    
    # Generate 30-day forecast with some randomness
    forecast = []
    current_price = base_price * season_factor["start"]
    
    # Trend direction (slight increase towards harvest)
    daily_change = (season_factor["end"] - season_factor["start"]) / 30
    
    np.random.seed(42)  # For reproducibility
    for day in range(30):
        # Add some random variation
        random_factor = 1 + np.random.uniform(-0.02, 0.02)
        current_price = current_price * (1 + daily_change) * random_factor
        forecast.append(round(current_price, 2))
    
    return forecast

def predict_price(crop_name: str, input_data: AnalysisInput) -> Dict:
    """
    Predict crop prices using LSTM model (simulated)
    Returns current price, predicted harvest price, and 30-day forecast
    """
    base_price = get_base_price(crop_name)
    
    # Generate forecast
    forecast = simulate_lstm_prediction(crop_name, input_data)
    
    # Determine trend
    if forecast[-1] > forecast[0] * 1.05:
        trend = "increasing"
    elif forecast[-1] < forecast[0] * 0.95:
        trend = "decreasing"
    else:
        trend = "stable"
    
    # Get prices at different intervals for the forecast summary
    forecast_summary = [
        round(forecast[6], 0),   # Week 1
        round(forecast[13], 0),  # Week 2
        round(forecast[20], 0),  # Week 3
        round(forecast[27], 0),  # Week 4
        round(forecast[29], 0)   # Day 30
    ]
    
    return {
        "current_price": round(base_price, 0),
        "predicted_price": round(forecast[-1], 0),
        "trend": trend,
        "forecast": forecast_summary,
        "full_forecast": forecast
    }

def get_historical_prices(crop_name: str, days: int = 60) -> List[Dict]:
    """
    Get historical price data (simulated)
    In production, this would fetch from database or API
    """
    base_price = get_base_price(crop_name)
    
    np.random.seed(123)
    prices = []
    current = base_price * 0.9  # Start lower
    
    from datetime import datetime, timedelta
    today = datetime.now()
    
    for i in range(days):
        date = today - timedelta(days=days-i)
        # Random walk with slight upward trend
        change = np.random.uniform(-0.02, 0.025)
        current = current * (1 + change)
        prices.append({
            "date": date.strftime("%Y-%m-%d"),
            "price": round(current, 2)
        })
    
    return prices
