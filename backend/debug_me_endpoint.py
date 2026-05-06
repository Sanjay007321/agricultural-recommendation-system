import requests
import traceback
import logging

# Enable debug logging
logging.basicConfig(level=logging.DEBUG)

def debug_me_endpoint():
    try:
        # Register a test user
        print("=== Registering test user ===")
        reg_data = {
            'full_name': 'Debug Test User',
            'mobile': '9990004444',
            'password': 'password123',
            'state': 'Tamil Nadu',
            'district': 'Erode'
        }
        
        reg_response = requests.post('http://localhost:8001/api/auth/register', json=reg_data)
        print(f"Registration status: {reg_response.status_code}")
        print(f"Registration response: {reg_response.text}")
        
        if reg_response.status_code == 200:
            token_data = reg_response.json()
            access_token = token_data['access_token']
            print(f"Got access token: {access_token[:20]}...")
            
            # Test the /me endpoint with the token
            print("\n=== Testing /me endpoint ===")
            headers = {'Authorization': f'Bearer {access_token}'}
            print(f"Headers: {headers}")
            
            me_response = requests.get('http://localhost:8001/api/auth/me', headers=headers)
            print(f"Me endpoint status: {me_response.status_code}")
            print(f"Me endpoint headers: {dict(me_response.headers)}")
            print(f"Me endpoint response: {me_response.text}")
            
            if me_response.status_code != 200:
                print(f"Error details: {me_response.text}")
        else:
            print(f"Registration failed: {reg_response.text}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    debug_me_endpoint()