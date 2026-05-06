import requests

# Try to login with an existing user
login_data = {
    'mobile': '9998887785',  # Use existing test user
    'password': 'password123'
}

login_response = requests.post('http://localhost:8001/api/auth/login', json=login_data)
print('Login status:', login_response.status_code)

if login_response.status_code == 200:
    token_data = login_response.json()
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
        print('Source:', data['current_weather']['source'])
        print('\nTop crop recommendations:')
        for i, crop in enumerate(data['top_crop_recommendations'], 1):
            print(f'{i}. {crop["crop"]} - {crop["suitability"].upper()}')
        print('\nWeather Analysis:')
        print('- Rainfall indication:', data['weather_analysis']['rainfall_indication'])
        print('- Temperature status:', data['weather_analysis']['temperature_status'])
        print('- Humidity level:', data['weather_analysis']['humidity_level'])
    else:
        print(f'Climate API Error: {climate_response.text}')
else:
    print(f'Login failed: {login_response.text}')
    
    # If login fails, try registering a new user with a different mobile
    reg_data = {
        'full_name': 'Test User 2',
        'mobile': '9998887788',
        'password': 'password123',
        'state': 'Tamil Nadu',
        'district': 'Chennai'
    }
    
    reg_response = requests.post('http://localhost:8001/api/auth/register', json=reg_data)
    print('Registration status:', reg_response.status_code)
    
    if reg_response.status_code == 200:
        token_data = reg_response.json()
        access_token = token_data['access_token']
        print('Got access token from registration')
        
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
            print('Source:', data['current_weather']['source'])
            print('\nTop crop recommendations:')
            for i, crop in enumerate(data['top_crop_recommendations'], 1):
                print(f'{i}. {crop["crop"]} - {crop["suitability"].upper()}')
            print('\nWeather Analysis:')
            print('- Rainfall indication:', data['weather_analysis']['rainfall_indication'])
            print('- Temperature status:', data['weather_analysis']['temperature_status'])
            print('- Humidity level:', data['weather_analysis']['humidity_level'])
        else:
            print(f'Climate API Error: {climate_response.text}')
    else:
        print(f'Registration failed: {reg_response.text}')