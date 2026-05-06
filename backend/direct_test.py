import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

# Force reload modules
import importlib
if 'app.services.climate_service' in sys.modules:
    importlib.reload(sys.modules['app.services.climate_service'])
if 'app.services.imd_weather_service' in sys.modules:
    importlib.reload(sys.modules['app.services.imd_weather_service'])

from app.services.climate_service import get_climate_dashboard_data
from app.services.imd_weather_service import get_imd_weather_data

print("=== Direct Function Test ===")

# Test IMD weather service directly
print("\n1. Testing IMD Weather Service:")
try:
    imd_data = get_imd_weather_data("Tamil Nadu", "Chennai")
    print(f"IMD Data Source: {imd_data.get('source', 'NOT FOUND')}")
    print(f"Temperature: {imd_data.get('current_temperature', 'NOT FOUND')}°C")
    print(f"Precipitation: {imd_data.get('precipitation', 'NOT FOUND')}mm")
    print(f"Humidity: {imd_data.get('humidity', 'NOT FOUND')}%")
except Exception as e:
    print(f"Error in IMD service: {e}")

# Test climate dashboard data
print("\n2. Testing Climate Dashboard Data:")
try:
    user_data = {
        "land_size": 1.0,
        "irrigation_type": "rainfed",
        "soil_type": "alluvial",
        "state": "Tamil Nadu",
        "district": "Chennai"
    }
    
    climate_data = get_climate_dashboard_data("Tamil Nadu", "Chennai", user_data)
    print(f"Climate Data Keys: {list(climate_data.keys())}")
    print(f"Current Weather Source: {climate_data['current_weather'].get('source', 'NOT FOUND')}")
    print(f"Weather Analysis Present: {'weather_analysis' in climate_data}")
    if 'weather_analysis' in climate_data:
        print(f"Rainfall Indication: {climate_data['weather_analysis'].get('rainfall_indication', 'NOT FOUND')}")
        print(f"Temperature Status: {climate_data['weather_analysis'].get('temperature_status', 'NOT FOUND')}")
        print(f"Humidity Level: {climate_data['weather_analysis'].get('humidity_level', 'NOT FOUND')}")
    else:
        print("ERROR: weather_analysis section is missing!")
        
    print(f"Soil Moisture 0-1cm: {climate_data['current_weather'].get('soil_moisture_0_1cm', 'NOT FOUND')}")
    print(f"Wind Speed 10m: {climate_data['current_weather'].get('wind_speed_10m', 'NOT FOUND')}")
    
except Exception as e:
    print(f"Error in climate service: {e}")
    import traceback
    traceback.print_exc()