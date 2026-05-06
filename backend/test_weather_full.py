import requests

# Login to get token
login_data = {'mobile': '9998887785', 'password': 'password123'}
login_response = requests.post('http://localhost:8001/api/auth/login', json=login_data)
token_data = login_response.json()
access_token = token_data['access_token']

# Test climate API with real weather data
headers = {'Authorization': f'Bearer {access_token}'}
climate_response = requests.get('http://localhost:8001/api/climate-dashboard', headers=headers)
print('Climate API status:', climate_response.status_code)
if climate_response.status_code == 200:
    data = climate_response.json()
    print('Real Weather Data:')
    weather = data['current_weather']
    print('Temperature:', weather['temperature'], '°C')
    print('Rainfall:', weather['rainfall'], 'mm')
    print('Humidity:', weather['humidity'], '%')
    print('Wind Speed:', weather.get('wind_speed', 'MISSING'), 'km/h')
    print('Wind Direction:', weather.get('wind_direction', 'MISSING'), 'degrees')
    print('Wind Speed 10m:', weather.get('wind_speed_10m', 'MISSING'), 'km/h')
    print('Wind Direction 10m:', weather.get('wind_direction_10m', 'MISSING'), 'degrees')
    print('Soil Moisture 0-1cm:', weather.get('soil_moisture_0_1cm', 'MISSING'))
    print('Soil Moisture 1-3cm:', weather.get('soil_moisture_1_3cm', 'MISSING'))
    print('Soil Moisture 3-9cm:', weather.get('soil_moisture_3_9cm', 'MISSING'))
    print('Soil Temperature 0cm:', weather.get('soil_temperature_0cm', 'MISSING'))
    print('Soil Temperature 6cm:', weather.get('soil_temperature_6cm', 'MISSING'))
    print('Soil Temperature 18cm:', weather.get('soil_temperature_18cm', 'MISSING'))
    print('Cloud Cover:', weather.get('cloud_cover', 'MISSING'))
    print('Visibility:', weather.get('visibility', 'MISSING'))
    print('Source:', weather.get('source', 'Unknown'))
    print('Coordinates:', weather.get('coordinates', 'None'))
    print('\nTop Recommendations:')
    for i, crop in enumerate(data['top_crop_recommendations'], 1):
        print(f'{i}. {crop["crop"]} - {crop["suitability"].upper()}')
else:
    print('Error:', climate_response.text)