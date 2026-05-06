import json
import os
import requests
from datetime import datetime
from typing import Dict, List, Optional

# Indian state coordinates mapping
INDIAN_STATES_COORDINATES = {
    "Tamil Nadu": {"latitude": 11.1271, "longitude": 78.6569},
    "Karnataka": {"latitude": 15.3173, "longitude": 75.7139},
    "Maharashtra": {"latitude": 19.7515, "longitude": 75.7139},
    "Uttar Pradesh": {"latitude": 26.8467, "longitude": 80.9462},
    "Punjab": {"latitude": 31.1471, "longitude": 75.3412},
    "West Bengal": {"latitude": 22.9868, "longitude": 87.8550},
    "Andhra Pradesh": {"latitude": 15.9129, "longitude": 79.7400},
    "Kerala": {"latitude": 10.8505, "longitude": 76.2711},
    "Gujarat": {"latitude": 22.2587, "longitude": 71.1924},
    "Rajasthan": {"latitude": 27.0238, "longitude": 74.2179},
    "Madhya Pradesh": {"latitude": 22.9734, "longitude": 78.6569},
    "Haryana": {"latitude": 29.0588, "longitude": 76.0856},
    "Bihar": {"latitude": 25.0961, "longitude": 85.3131},
    "Odisha": {"latitude": 20.9517, "longitude": 85.0985},
    "Chhattisgarh": {"latitude": 21.2787, "longitude": 81.8661},
    "Jharkhand": {"latitude": 23.6102, "longitude": 85.2799},
    "Assam": {"latitude": 26.2006, "longitude": 92.9376},
    "Telangana": {"latitude": 18.1124, "longitude": 79.0193},
    "Delhi": {"latitude": 28.7041, "longitude": 77.1025},
    "Jammu and Kashmir": {"latitude": 33.7782, "longitude": 76.5762}
}

def get_current_weather_data(state: str, district: str) -> Dict:
    """
    Get comprehensive current weather data using IMD API integration
    This function now exclusively uses the real IMD API without any Open-Meteo fallback
    """
    print(f"DEBUG: get_current_weather_data called for {state}, {district}")
    try:
        # Import the IMD weather service
        from app.services.imd_weather_service import get_imd_weather_data
        
        # Get data from the real IMD API
        imd_weather_data = get_imd_weather_data(state, district)
        print(f"DEBUG: Successfully fetched data from IMD API: {imd_weather_data.get('source', 'Unknown source')}")
        
        # Transform IMD data to our expected format
        result = {
            "current_temp": imd_weather_data.get("current_temperature", 0),
            "current_rainfall": imd_weather_data.get("precipitation", 0),
            "current_precipitation": imd_weather_data.get("precipitation", 0),
            "humidity": imd_weather_data.get("humidity", 65),
            "cloud_cover": imd_weather_data.get("cloud_cover", 20),
            "visibility": imd_weather_data.get("visibility", 10000),
            "weather_code": imd_weather_data.get("current_weather_code", 0),
            "temp_max": imd_weather_data.get("max_temperature", 0),
            "temp_min": imd_weather_data.get("min_temperature", 0),
            "sunrise": imd_weather_data.get("sunrise", "06:00"),
            "sunset": imd_weather_data.get("sunset", "18:00"),
            "rain_sum": imd_weather_data.get("rain_sum", 0),
            "wind_speed_10m": imd_weather_data.get("current_windspeed", 0),
            "wind_direction_10m": imd_weather_data.get("current_wind_direction", 0),
            "region_type": _get_region_type(state),
            "updated_at": imd_weather_data.get("updated_at"),
            "source": imd_weather_data.get("source"),
            "coordinates": imd_weather_data.get("coordinates", {}),
            # Soil moisture and temperature parameters (not available in current IMD API)
            "soil_moisture_0_1cm": imd_weather_data.get("soil_moisture_0_1cm", 0),
            "soil_moisture_1_3cm": imd_weather_data.get("soil_moisture_1_3cm", 0),
            "soil_moisture_3_9cm": imd_weather_data.get("soil_moisture_3_9cm", 0),
            "soil_temperature_0cm": imd_weather_data.get("soil_temperature_0cm", 0),
            "soil_temperature_6cm": imd_weather_data.get("soil_temperature_6cm", 0),
            "soil_temperature_18cm": imd_weather_data.get("soil_temperature_18cm", 0),
            "wind_speed": imd_weather_data.get("current_windspeed", 0),  # Duplicate for compatibility
            "wind_direction": imd_weather_data.get("current_wind_direction", 0)  # Duplicate for compatibility
        }
        
        print(f"DEBUG: Returning weather data with source: {result['source']}")
        return result
        
    except requests.exceptions.RequestException as e:
        print(f"Network error fetching weather data: {e}")
        # Fallback to mock data if API fails
        return get_mock_weather_data(state, district)
    except Exception as e:
        print(f"Unexpected error in weather service: {e}")
        # Fallback to mock data
        return get_mock_weather_data(state, district)

def _get_region_type(state: str) -> str:
    """
    Helper function to determine region type based on state
    """
    region_types = {
        "Tamil Nadu": "tropical",
        "Kerala": "tropical", 
        "Karnataka": "tropical",
        "West Bengal": "tropical",
        "Assam": "tropical",
        "Odisha": "tropical",
        "Andhra Pradesh": "tropical",
        "Telangana": "tropical",
        "Maharashtra": "semi-arid",
        "Gujarat": "semi-arid",
        "Rajasthan": "arid",
        "Punjab": "semi-arid",
        "Haryana": "semi-arid",
        "Uttar Pradesh": "subtropical",
        "Madhya Pradesh": "tropical",
        "Chhattisgarh": "tropical",
        "Jharkhand": "tropical",
        "Bihar": "subtropical",
        "Delhi": "subtropical",
        "Jammu and Kashmir": "temperate"
    }
    
    return region_types.get(state, "tropical")

def get_mock_weather_data(state: str, district: str) -> Dict:
    """
    Fallback mock weather data when API is unavailable
    """
    # Mock weather data for different Indian regions
    weather_data = {
        "Tamil Nadu": {
            "current_temp": 32.5,
            "current_rainfall": 45.2,
            "humidity": 65,
            "region_type": "tropical"
        },
        "Karnataka": {
            "current_temp": 28.3,
            "current_rainfall": 78.5,
            "humidity": 60,
            "region_type": "tropical"
        },
        "Maharashtra": {
            "current_temp": 30.1,
            "current_rainfall": 22.8,
            "humidity": 55,
            "region_type": "semi-arid"
        },
        "Uttar Pradesh": {
            "current_temp": 25.7,
            "current_rainfall": 15.3,
            "humidity": 50,
            "region_type": "subtropical"
        },
        "Punjab": {
            "current_temp": 22.4,
            "current_rainfall": 8.7,
            "humidity": 45,
            "region_type": "semi-arid"
        },
        "West Bengal": {
            "current_temp": 29.8,
            "current_rainfall": 156.3,
            "humidity": 75,
            "region_type": "tropical"
        }
    }
    
    # Get base data for state
    state_data = weather_data.get(state, {
        "current_temp": 26.0,
        "current_rainfall": 50.0,
        "humidity": 60,
        "region_type": "tropical"
    })
    
    # Adjust based on district and season (mock adjustment)
    import random
    seasonal_factor = random.uniform(0.9, 1.1)  # Random variation
    adjusted_temp = round(state_data["current_temp"] * seasonal_factor, 1)
    adjusted_rainfall = round(state_data["current_rainfall"] * seasonal_factor, 1)
    
    return {
        "current_temp": adjusted_temp,
        "current_rainfall": adjusted_rainfall,
        "current_precipitation": adjusted_rainfall,
        "humidity": state_data["humidity"],
        "cloud_cover": round(random.uniform(20, 80)),
        "visibility": round(random.uniform(5000, 15000)),
        "weather_code": round(random.uniform(0, 3)),
        "temp_max": round(adjusted_temp + random.uniform(2, 5), 1),
        "temp_min": round(adjusted_temp - random.uniform(2, 5), 1),
        "sunrise": "06:15",
        "sunset": "18:30",
        "rain_sum": adjusted_rainfall,
        "wind_speed_10m": round(random.uniform(5, 15), 1),
        "wind_direction_10m": round(random.uniform(0, 360)),
        "region_type": state_data["region_type"],
        "updated_at": datetime.now().isoformat(),
        "source": "Mock Data",
        "coordinates": {"latitude": 22.0, "longitude": 79.0}
    }

def get_crop_climate_requirements() -> Dict:
    """Get climate requirements for different crops"""
    # Crop climate requirements based on Indian agricultural data
    return {
        "Rice": {
            "optimal_temp": (25, 35),  # Celsius
            "min_temp": 20,
            "optimal_rainfall": (1000, 2500),  # mm
            "min_rainfall": 500,
            "climate": "tropical",
            "season": "kharif",
            "soil_type": "alluvial",
            "major_varieties": ["IR 64", "Basmati 370", "Swarna", "Punjab Basmati"]
        },
        "Wheat": {
            "optimal_temp": (15, 25),
            "min_temp": 10,
            "optimal_rainfall": (300, 600),
            "min_rainfall": 200,
            "climate": "temperate",
            "season": "rabi",
            "soil_type": "loamy",
            "major_varieties": ["HD 2967", "PBW 343", "WH 1105", "MACS 6222"]
        },
        "Maize": {
            "optimal_temp": (20, 30),
            "min_temp": 15,
            "optimal_rainfall": (600, 1200),
            "min_rainfall": 400,
            "climate": "tropical",
            "season": "kharif",
            "soil_type": "well-drained",
            "major_varieties": ["Deccan Hybrid", "Pioneer 30Y87", "Himalayan 123", "PMH 1"]
        },
        "Cotton": {
            "optimal_temp": (25, 35),
            "min_temp": 20,
            "optimal_rainfall": (500, 1000),
            "min_rainfall": 400,
            "climate": "semi-arid",
            "season": "kharif",
            "soil_type": "black cotton",
            "major_varieties": ["Bt Cotton", "Shankar 6", "Gujarat Cotton", "FC 3"]
        },
        "Sugarcane": {
            "optimal_temp": (25, 35),
            "min_temp": 20,
            "optimal_rainfall": (1200, 2500),
            "min_rainfall": 1000,
            "climate": "tropical",
            "season": "perennial",
            "soil_type": "fertile",
            "major_varieties": ["Co 270", "Co 419", "CoS 767", "BO 91"]
        }
    }

def compare_crop_conditions(user_data: dict, weather_data: dict) -> List[Dict]:
    """
    Compare user's current climate with crop requirements
    """
    crops_data = get_crop_climate_requirements()
    user_temp = weather_data.get("current_temp", 0)
    user_rainfall = weather_data.get("current_rainfall", 0)
    user_humidity = weather_data.get("humidity", 65)
    user_soil_moisture_0_1cm = weather_data.get("soil_moisture_0_1cm", 0)
    user_soil_moisture_1_3cm = weather_data.get("soil_moisture_1_3cm", 0)
    user_soil_moisture_3_9cm = weather_data.get("soil_moisture_3_9cm", 0)
    user_wind_speed = weather_data.get("wind_speed", 0)
    user_wind_direction = weather_data.get("wind_direction", 0)
    
    recommendations = []
    
    for crop, req in crops_data.items():
        # Temperature assessment
        optimal_temp = req["optimal_temp"]
        if optimal_temp[0] <= user_temp <= optimal_temp[1]:
            temp_status = "ideal"
            temp_recommendation = f"Current temperature ({user_temp}°C) is perfect for {crop}"
        elif req["min_temp"] <= user_temp:
            temp_status = "moderate"
            temp_recommendation = f"Current temperature ({user_temp}°C) is acceptable, but may require attention during critical growth phases"
        else:
            temp_status = "risk"
            temp_recommendation = f"Current temperature ({user_temp}°C) may cause damage or delays - requires proper protection mechanisms"
            
        # Rainfall assessment
        if user_data.get('irrigation_type') == 'irrigated':
            # For irrigated land, rainfall is less critical
            rainfall_status = "adequate"
            rainfall_recommendation = f"Land is irrigated, so rainfall ({user_rainfall}mm) is supplementary"
            optimal_rainfall = req["optimal_rainfall"]  # Define here for later use
        else:
            optimal_rainfall = req["optimal_rainfall"]  # Define here for later use
            if optimal_rainfall[0] <= user_rainfall <= optimal_rainfall[1]:
                rainfall_status = "ideal"
                rainfall_recommendation = f"Current rainfall ({user_rainfall}mm) is optimal for {crop}"
            elif req["min_rainfall"] <= user_rainfall:
                rainfall_status = "moderate"
                rainfall_recommendation = f"Current rainfall ({user_rainfall}mm) is acceptable, but may need irrigation support"
            else:
                rainfall_status = "risk"
                rainfall_recommendation = f"Current rainfall ({user_rainfall}mm) is insufficient - irrigation is essential"
        
        # Humidity assessment (added for better crop analysis)
        humidity_status = "moderate"
        if crop in ["Rice", "Sugarcane"] and user_humidity > 70:
            humidity_status = "ideal"
            humidity_recommendation = f"High humidity ({user_humidity}%) is beneficial for {crop}"
        elif crop in ["Wheat", "Cotton"] and 40 <= user_humidity <= 60:
            humidity_status = "ideal"
            humidity_recommendation = f"Moderate humidity ({user_humidity}%) is ideal for {crop}"
        else:
            humidity_recommendation = f"Humidity ({user_humidity}%) is within acceptable range for {crop}"
        
        # Soil moisture assessment (added for better crop analysis)
        soil_moisture_status = "moderate"
        avg_soil_moisture = (user_soil_moisture_0_1cm + user_soil_moisture_1_3cm + user_soil_moisture_3_9cm) / 3
        if avg_soil_moisture > 0:  # If we have actual soil moisture data
            if crop in ["Rice", "Sugarcane"] and avg_soil_moisture > 0.3:  # Wet conditions preferred
                soil_moisture_status = "ideal"
                soil_moisture_recommendation = f"Soil moisture levels are adequate for {crop}"
            elif crop in ["Wheat", "Cotton"] and 0.1 <= avg_soil_moisture <= 0.4:  # Moderate moisture
                soil_moisture_status = "ideal"
                soil_moisture_recommendation = f"Soil moisture levels are optimal for {crop}"
            else:
                soil_moisture_recommendation = f"Soil moisture levels are acceptable for {crop} but monitor closely"
        else:
            soil_moisture_recommendation = f"No specific soil moisture data - rely on rainfall and irrigation"
        
        # Overall suitability - considering multiple factors
        factor_count = 0
        positive_factors = 0
        
        if temp_status == "ideal":
            positive_factors += 1
        elif temp_status == "moderate":
            positive_factors += 0.5
        factor_count += 1
        
        if rainfall_status == "ideal":
            positive_factors += 1
        elif rainfall_status == "moderate":
            positive_factors += 0.5
        factor_count += 1
        
        if humidity_status == "ideal":
            positive_factors += 1
        elif humidity_status == "moderate":
            positive_factors += 0.5
        factor_count += 1
        
        if soil_moisture_status == "ideal":
            positive_factors += 1
        elif soil_moisture_status == "moderate":
            positive_factors += 0.5
        factor_count += 1
        
        # Calculate suitability based on percentage of positive factors
        suitability_ratio = positive_factors / factor_count
        
        if suitability_ratio >= 0.8:
            suitability = "excellent"
            overall_recommendation = f"Excellent conditions for {crop} cultivation - all major factors are favorable"
        elif suitability_ratio >= 0.6:
            suitability = "good"
            overall_recommendation = f"Good conditions for {crop} - most factors are favorable"
        elif suitability_ratio >= 0.4:
            suitability = "caution"
            overall_recommendation = f"{crop} cultivation requires careful management - some factors are suboptimal"
        else:
            suitability = "poor"
            overall_recommendation = f"{crop} cultivation not recommended under current conditions - multiple factors are unfavorable"
            
        recommendations.append({
            "crop": crop,
            "suitability": suitability,
            "temperature_status": temp_status,
            "rainfall_status": rainfall_status,
            "humidity_status": humidity_status,
            "soil_moisture_status": soil_moisture_status,
            "temperature_recommendation": temp_recommendation,
            "rainfall_recommendation": rainfall_recommendation,
            "humidity_recommendation": humidity_recommendation,
            "soil_moisture_recommendation": soil_moisture_recommendation,
            "overall_recommendation": overall_recommendation,
            "major_varieties": req["major_varieties"],
            "optimal_temp_range": f"{optimal_temp[0]}-{optimal_temp[1]}°C",
            "optimal_rainfall_range": f"{optimal_rainfall[0]}-{optimal_rainfall[1]}mm",
            "current_temp": user_temp,
            "current_rainfall": user_rainfall,
            "current_humidity": user_humidity,
            "current_soil_moisture": avg_soil_moisture if avg_soil_moisture > 0 else None
        })
        
    return recommendations

def get_climate_dashboard_data(user_state: str, user_district: str, user_data: dict) -> Dict:
    """
    Get comprehensive climate data for dashboard display
    """
    print("DEBUG: get_climate_dashboard_data function called!")
    # Get current weather data
    weather_data = get_current_weather_data(user_state, user_district)
    
    print(f"Weather data keys: {list(weather_data.keys())}")
    print(f"Soil moisture 0-1cm in weather_data: {weather_data.get('soil_moisture_0_1cm', 'NOT FOUND')}")
    print(f"Wind speed 10m in weather_data: {weather_data.get('wind_speed_10m', 'NOT FOUND')}")
    
    # Get crop recommendations
    crop_recommendations = compare_crop_conditions(user_data, weather_data)
    
    # Get top 3 recommended crops
    top_recommendations = sorted(
        crop_recommendations, 
        key=lambda x: {"excellent": 4, "good": 3, "caution": 2, "poor": 1}[x["suitability"]], 
        reverse=True
    )[:3]
    
    return {
        "current_weather": {
            "temperature": weather_data["current_temp"],
            "rainfall": weather_data["current_rainfall"],
            "humidity": weather_data["humidity"],
            "region_type": weather_data["region_type"],
            "updated_at": weather_data["updated_at"],
            "source": weather_data["source"],
            "coordinates": weather_data.get("coordinates", {}),
            # Additional weather parameters from new API
            "current_precipitation": weather_data.get("current_precipitation", 0),
            "cloud_cover": weather_data.get("cloud_cover", 0),
            "visibility": weather_data.get("visibility", 0),
            "weather_code": weather_data.get("weather_code", 0),
            "temp_max": weather_data.get("temp_max", 0),
            "temp_min": weather_data.get("temp_min", 0),
            "sunrise": weather_data.get("sunrise", "06:00"),
            "sunset": weather_data.get("sunset", "18:00"),
            "rain_sum": weather_data.get("rain_sum", 0),
            "wind_speed_10m": weather_data.get("wind_speed_10m", 0),
            "wind_direction_10m": weather_data.get("wind_direction_10m", 0),
            # Soil moisture parameters
            "soil_moisture_0_1cm": weather_data.get("soil_moisture_0_1cm", 0),
            "soil_moisture_1_3cm": weather_data.get("soil_moisture_1_3cm", 0),
            "soil_moisture_3_9cm": weather_data.get("soil_moisture_3_9cm", 0),
            "soil_temperature_0cm": weather_data.get("soil_temperature_0cm", 0),
            "soil_temperature_6cm": weather_data.get("soil_temperature_6cm", 0),
            "soil_temperature_18cm": weather_data.get("soil_temperature_18cm", 0),
            "wind_speed": weather_data.get("wind_speed", 0),
            "wind_direction": weather_data.get("wind_direction", 0)
        },
        "top_crop_recommendations": top_recommendations,
        "all_recommendations": crop_recommendations,
        "location": {
            "state": user_state,
            "district": user_district
        },
        "weather_analysis": {
            "rainfall_indication": _get_rainfall_indication(weather_data.get("current_rainfall", 0)),
            "temperature_status": _get_temperature_status(weather_data.get("current_temp", 25)),
            "humidity_level": _get_humidity_level(weather_data.get("humidity", 65))
        }
    }


def _get_rainfall_indication(rainfall: float) -> str:
    """
    Get rainfall indication based on amount
    """
    if rainfall == 0:
        return "No rainfall today"
    elif rainfall < 2.5:
        return "Light rainfall - beneficial for crops"
    elif rainfall < 7.5:
        return "Moderate rainfall - good for irrigation"
    elif rainfall < 15:
        return "Heavy rainfall - monitor for waterlogging"
    else:
        return "Very heavy rainfall - risk of flooding/damage"


def _get_temperature_status(temp: float) -> str:
    """
    Get temperature status based on value
    """
    if temp < 10:
        return "Cold conditions - protect crops from frost"
    elif temp < 20:
        return "Cool conditions - suitable for rabi crops"
    elif temp < 30:
        return "Optimal conditions - good for most crops"
    elif temp < 35:
        return "Warm conditions - ensure adequate irrigation"
    else:
        return "Hot conditions - immediate irrigation and protection needed"


def _get_humidity_level(humidity: float) -> str:
    """
    Get humidity level description
    """
    if humidity < 30:
        return "Low humidity - increased irrigation required"
    elif humidity < 60:
        return "Moderate humidity - balanced conditions"
    else:
        return "High humidity - watch for fungal diseases"
