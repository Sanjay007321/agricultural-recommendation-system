import requests
import json

print("Testing registration with a new mobile number...")
url = 'http://localhost:8001/api/auth/register'
payload = {
    'full_name': 'Test User',
    'mobile': '9123456789',
    'password': 'password123',
    'state': 'Maharashtra',
    'district': 'Pune',
    'village': 'Test Village',
    'land_size_acres': 5.5
}

try:
    response = requests.post(url, json=payload)
    print('Status Code:', response.status_code)
    print('Response:', response.text)
except Exception as e:
    print('Error:', e)

print("\nTesting registration with the same mobile number (should fail with duplicate error)...")
payload_duplicate = {
    'full_name': 'Another Test User',
    'mobile': '9123456789',
    'password': 'password456',
    'state': 'Karnataka',
    'district': 'Bangalore',
    'village': 'Test Village 2',
    'land_size_acres': 3.2
}

try:
    response = requests.post(url, json=payload_duplicate)
    print('Status Code:', response.status_code)
    print('Response:', response.text)
except Exception as e:
    print('Error:', e)