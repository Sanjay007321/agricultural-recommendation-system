import requests

def test_endpoints():
    # Test the /me endpoint
    print("=== Testing /me endpoint ===")
    
    # First, register a user to get a token
    reg_data = {
        'full_name': 'CORS Test User',
        'mobile': '7778881111',
        'password': 'password123',
        'state': 'Tamil Nadu',
        'district': 'Erode'
    }
    
    try:
        reg_response = requests.post('http://localhost:8001/api/auth/register', json=reg_data)
        print(f"Registration status: {reg_response.status_code}")
        
        if reg_response.status_code == 200:
            token_data = reg_response.json()
            access_token = token_data['access_token']
            print("Got access token successfully")
            
            # Test the /me endpoint with the token
            headers = {'Authorization': f'Bearer {access_token}'}
            me_response = requests.get('http://localhost:8001/api/auth/me', headers=headers)
            print(f"Me endpoint status: {me_response.status_code}")
            
            if me_response.status_code == 200:
                print("✓ /me endpoint works correctly!")
                print(f"User data: {me_response.json()}")
            else:
                print(f"✗ /me endpoint failed: {me_response.text}")
        else:
            print(f"Registration failed: {reg_response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_endpoints()