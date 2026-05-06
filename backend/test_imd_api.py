"""
Test script to verify IMD API integration is working correctly
This tests the new IMD-only weather service implementation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

def test_imd_weather_service():
    """Test the IMD weather service directly"""
    print("Testing IMD Weather Service Integration...")
    print("=" * 50)
    
    try:
        from app.services.imd_weather_service import get_imd_weather_data
        
        # Test with different locations
        test_cases = [
            ("Tamil Nadu", "Chennai"),
            ("Maharashtra", "Mumbai"),
            ("Karnataka", "Bangalore"),
            ("Uttar Pradesh", "Lucknow")
        ]
        
        for state, district in test_cases:
            print(f"\nTesting: {district}, {state}")
            print("-" * 30)
            
            try:
                weather_data = get_imd_weather_data(state, district)
                
                print(f"Source: {weather_data.get('source', 'Unknown')}")
                print(f"Location: {weather_data.get('location', 'Unknown')}")
                print(f"Current Temperature: {weather_data.get('current_temperature', 'N/A')}°C")
                print(f"Precipitation: {weather_data.get('precipitation', 'N/A')}mm")
                print(f"Humidity: {weather_data.get('humidity', 'N/A')}%")
                print(f"Max Temperature: {weather_data.get('max_temperature', 'N/A')}°C")
                print(f"Min Temperature: {weather_data.get('min_temperature', 'N/A')}°C")
                print(f"Sunrise: {weather_data.get('sunrise', 'N/A')}")
                print(f"Sunset: {weather_data.get('sunset', 'N/A')}")
                
                # Check if soil moisture data is present (should be 0 as placeholders)
                soil_moisture_0_1cm = weather_data.get('soil_moisture_0_1cm', 'MISSING')
                wind_speed = weather_data.get('current_windspeed', 'MISSING')
                
                print(f"Soil Moisture 0-1cm: {soil_moisture_0_1cm}")
                print(f"Wind Speed: {wind_speed}")
                
                if soil_moisture_0_1cm == 0 and wind_speed == 0:
                    print("✓ Soil moisture and wind data are properly handled as placeholders")
                else:
                    print("⚠ Unexpected values for soil moisture or wind data")
                    
            except Exception as e:
                print(f"Error testing {district}: {e}")
                
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def test_climate_service():
    """Test the climate service with IMD integration"""
    print("\n\nTesting Climate Service with IMD Integration...")
    print("=" * 50)
    
    try:
        from app.services.climate_service import get_climate_dashboard_data
        
        # Mock user data for testing
        user_data = {
            "region_type": "tropical",
            "irrigation_type": "irrigated"
        }
        
        test_cases = [
            ("Tamil Nadu", "Chennai"),
            ("Maharashtra", "Mumbai")
        ]
        
        for state, district in test_cases:
            print(f"\nTesting Climate Dashboard: {district}, {state}")
            print("-" * 40)
            
            try:
                climate_data = get_climate_dashboard_data(state, district, user_data)
                
                # Check weather data
                current_weather = climate_data.get("current_weather", {})
                print(f"Temperature: {current_weather.get('temperature', 'N/A')}°C")
                print(f"Rainfall: {current_weather.get('rainfall', 'N/A')}mm")
                print(f"Humidity: {current_weather.get('humidity', 'N/A')}%")
                print(f"Source: {current_weather.get('source', 'N/A')}")
                
                # Check soil moisture and wind data
                soil_moisture_0_1cm = current_weather.get('soil_moisture_0_1cm', 'MISSING')
                wind_speed = current_weather.get('wind_speed', 'MISSING')
                wind_speed_10m = current_weather.get('wind_speed_10m', 'MISSING')
                
                print(f"Soil Moisture 0-1cm: {soil_moisture_0_1cm}")
                print(f"Wind Speed: {wind_speed}")
                print(f"Wind Speed 10m: {wind_speed_10m}")
                
                # Check weather analysis
                weather_analysis = climate_data.get("weather_analysis", {})
                print(f"Rainfall Indication: {weather_analysis.get('rainfall_indication', 'N/A')}")
                print(f"Temperature Status: {weather_analysis.get('temperature_status', 'N/A')}")
                print(f"Humidity Level: {weather_analysis.get('humidity_level', 'N/A')}")
                
                # Check crop recommendations
                top_recommendations = climate_data.get("top_crop_recommendations", [])
                print(f"Top Recommendations Count: {len(top_recommendations)}")
                if top_recommendations:
                    print(f"Best Crop: {top_recommendations[0].get('crop', 'N/A')}")
                    print(f"Suitability: {top_recommendations[0].get('suitability', 'N/A')}")
                
                print("✓ Climate service test completed successfully")
                
            except Exception as e:
                print(f"Error testing climate service for {district}: {e}")
                
    except ImportError as e:
        print(f"Import error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def test_api_integration():
    """Test the complete API integration"""
    print("\n\nTesting Complete API Integration...")
    print("=" * 50)
    
    try:
        import requests
        import json
        
        # Test if the backend server is running
        try:
            response = requests.get("http://localhost:8001/docs", timeout=5)
            if response.status_code == 200:
                print("✓ Backend server is running")
                
                # Test registration/login to get auth token
                reg_data = {
                    'mobile': '9998887785',
                    'password': 'password123',
                    'state': 'Tamil Nadu',
                    'district': 'Chennai'
                }
                
                # Try to register (might fail if already exists)
                try:
                    reg_response = requests.post('http://localhost:8001/api/auth/register', json=reg_data)
                    if reg_response.status_code == 200:
                        print("✓ User registered successfully")
                    else:
                        print("ℹ User registration failed (may already exist)")
                except:
                    print("ℹ Registration test skipped")
                
                # Try to login
                login_data = {
                    'mobile': '9998887785',
                    'password': 'password123'
                }
                
                try:
                    login_response = requests.post('http://localhost:8001/api/auth/login', json=login_data)
                    if login_response.status_code == 200:
                        auth_data = login_response.json()
                        access_token = auth_data.get('access_token')
                        print("✓ User login successful")
                        
                        if access_token:
                            headers = {'Authorization': f'Bearer {access_token}'}
                            
                            # Test climate dashboard API
                            try:
                                climate_response = requests.get(
                                    'http://localhost:8001/api/analysis/climate-dashboard', 
                                    headers=headers
                                )
                                
                                if climate_response.status_code == 200:
                                    climate_data = climate_response.json()
                                    print("✓ Climate dashboard API call successful")
                                    
                                    # Check the response structure
                                    current_weather = climate_data.get("current_weather", {})
                                    weather_analysis = climate_data.get("weather_analysis", {})
                                    
                                    print(f"  Temperature: {current_weather.get('temperature', 'N/A')}°C")
                                    print(f"  Rainfall: {current_weather.get('rainfall', 'N/A')}mm")
                                    print(f"  Source: {current_weather.get('source', 'N/A')}")
                                    print(f"  Rainfall Indication: {weather_analysis.get('rainfall_indication', 'N/A')}")
                                    
                                    # Check if soil moisture and wind data are present
                                    soil_moisture = current_weather.get('soil_moisture_0_1cm', 'MISSING')
                                    wind_speed = current_weather.get('wind_speed', 'MISSING')
                                    print(f"  Soil Moisture 0-1cm: {soil_moisture}")
                                    print(f"  Wind Speed: {wind_speed}")
                                    
                                else:
                                    print(f"✗ Climate dashboard API failed: {climate_response.status_code}")
                                    print(f"  Response: {climate_response.text}")
                                    
                            except Exception as e:
                                print(f"✗ Climate dashboard API test failed: {e}")
                        else:
                            print("✗ No access token received")
                    else:
                        print(f"✗ Login failed: {login_response.status_code}")
                        
                except Exception as e:
                    print(f"✗ Login test failed: {e}")
            else:
                print("✗ Backend server is not responding properly")
                
        except requests.exceptions.ConnectionError:
            print("✗ Backend server is not running. Please start the server first.")
        except Exception as e:
            print(f"✗ Server test failed: {e}")
            
    except ImportError:
        print("⚠ requests library not available for API testing")
    except Exception as e:
        print(f"✗ API integration test failed: {e}")

if __name__ == "__main__":
    print("IMD API Integration Test Suite")
    print("=" * 60)
    
    # Run all tests
    test_imd_weather_service()
    test_climate_service()
    test_api_integration()
    
    print("\n" + "=" * 60)
    print("Test suite completed!")