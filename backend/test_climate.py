import requests

# Register a test user
reg_data = {
    'full_name': 'Climate Test User',
    'mobile': '1112223333',
    'password': 'password123',
    'state': 'Tamil Nadu',
    'district': 'Erode'
}

reg_response = requests.post('http://localhost:8001/api/auth/register', json=reg_data)
print('Registration status:', reg_response.status_code)

if reg_response.status_code == 200:
    token_data = reg_response.json()
    access_token = token_data['access_token']
    print('Got access token')
    
    # Test climate API
    headers = {'Authorization': f'Bearer {access_token}'}
    climate_response = requests.get('http://localhost:8001/api/climate-dashboard', headers=headers)
    print('Climate API status:', climate_response.status_code)
    
    if climate_response.status_code == 200:
        data = climate_response.json()
        print('Climate data retrieved successfully!')
        print('Current temperature:', data['current_weather']['temperature'], '°C')
        print('Current rainfall:', data['current_weather']['rainfall'], 'mm')
        print('Humidity:', data['current_weather']['humidity'], '%')
        print('Region type:', data['current_weather']['region_type'])
        print('\nTop crop recommendations:')
        for i, crop in enumerate(data['top_crop_recommendations'], 1):
            print(f'{i}. {crop["crop"]} - {crop["suitability"].upper()}')
            print(f'   Temp range: {crop["optimal_temp_range"]}')
            print(f'   Rainfall range: {crop["optimal_rainfall_range"]}')
            print(f'   Varieties: {", ".join(crop["major_varieties"][:2])}...')
            print()
    else:
        print('Error:', climate_response.text)
else:
    print('Registration failed:', reg_response.text)