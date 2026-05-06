import requests

# Login to get token
login_data = {'mobile': '1112223333', 'password': 'password123'}
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
    print('Temperature:', data['current_weather']['temperature'], '°C')
    print('Rainfall:', data['current_weather']['rainfall'], 'mm')
    print('Humidity:', data['current_weather']['humidity'], '%')
    print('Source:', data['current_weather'].get('source', 'Unknown'))
    print('Top Recommendations:')
    for i, crop in enumerate(data['top_crop_recommendations'], 1):
        print(f'{i}. {crop["crop"]} - {crop["suitability"].upper()}')
else:
    print('Error:', climate_response.text)