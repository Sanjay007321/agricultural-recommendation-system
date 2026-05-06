import requests
import json

def test_registration_flow():
    """Test the complete registration flow with debugging"""
    
    print("=== REGISTRATION FLOW TEST ===")
    
    # Test data
    test_data = {
        "full_name": "Debug Test User",
        "mobile": "5555555555",
        "password": "password123",
        "state": "Tamil Nadu",
        "district": "Erode"
    }
    
    print("Test data:", test_data)
    
    # Step 1: Get states to verify state/district data
    print("\n1. Testing state/district data...")
    try:
        states_response = requests.get('http://localhost:8001/api/states')
        if states_response.status_code == 200:
            states_data = states_response.json()
            print(f"✓ Got {len(states_data)} states")
            
            # Find Tamil Nadu
            tn_state = None
            for state in states_data:
                if state['name'] == 'Tamil Nadu':
                    tn_state = state
                    break
            
            if tn_state:
                print(f"✓ Found Tamil Nadu with {len(tn_state['districts'])} districts")
                print(f"✓ Erode in districts: {'Erode' in tn_state['districts']}")
                if 'Erode' in tn_state['districts']:
                    print("✓ State/district validation should pass")
                else:
                    print("✗ Erode not found in Tamil Nadu districts")
                    return False
            else:
                print("✗ Tamil Nadu not found")
                return False
        else:
            print(f"✗ Failed to get states: {states_response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Error getting states: {e}")
        return False
    
    # Step 2: Test registration
    print("\n2. Testing registration...")
    try:
        register_response = requests.post(
            'http://localhost:8001/api/auth/register',
            json=test_data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"Registration response status: {register_response.status_code}")
        print(f"Registration response: {register_response.text}")
        
        if register_response.status_code == 200:
            print("✓ Registration successful!")
            response_data = register_response.json()
            print(f"Farmer ID: {response_data.get('farmer_id')}")
            return True
        else:
            print("✗ Registration failed")
            return False
            
    except Exception as e:
        print(f"✗ Error during registration: {e}")
        return False

def test_frontend_validation():
    """Test the validation logic that might be failing in frontend"""
    
    print("\n=== FRONTEND VALIDATION TEST ===")
    
    # Simulate the validation logic
    test_cases = [
        {
            "name": "Valid data",
            "data": {
                "full_name": "Test User",
                "mobile": "5555555555",
                "password": "password123",
                "confirmPassword": "password123",
                "state": "Tamil Nadu",
                "district": "Erode",
                "aadhar_number": "123456789012"
            }
        },
        {
            "name": "Missing full name",
            "data": {
                "full_name": "",
                "mobile": "5555555555",
                "password": "password123",
                "confirmPassword": "password123",
                "state": "Tamil Nadu",
                "district": "Erode"
            }
        },
        {
            "name": "Invalid mobile",
            "data": {
                "full_name": "Test User",
                "mobile": "123",
                "password": "password123",
                "confirmPassword": "password123",
                "state": "Tamil Nadu",
                "district": "Erode"
            }
        },
        {
            "name": "Password mismatch",
            "data": {
                "full_name": "Test User",
                "mobile": "5555555555",
                "password": "password123",
                "confirmPassword": "different",
                "state": "Tamil Nadu",
                "district": "Erode"
            }
        },
        {
            "name": "Invalid Aadhar",
            "data": {
                "full_name": "Test User",
                "mobile": "5555555555",
                "password": "password123",
                "confirmPassword": "password123",
                "state": "Tamil Nadu",
                "district": "Erode",
                "aadhar_number": "12345"
            }
        },
        {
            "name": "Missing state",
            "data": {
                "full_name": "Test User",
                "mobile": "5555555555",
                "password": "password123",
                "confirmPassword": "password123",
                "state": "",
                "district": "Erode"
            }
        },
        {
            "name": "Missing district",
            "data": {
                "full_name": "Test User",
                "mobile": "5555555555",
                "password": "password123",
                "confirmPassword": "password123",
                "state": "Tamil Nadu",
                "district": ""
            }
        }
    ]
    
    for test_case in test_cases:
        print(f"\nTesting: {test_case['name']}")
        data = test_case['data']
        
        # Validate form data (similar to frontend logic)
        errors = []
        
        if not data.get('full_name', '').strip():
            errors.append('Full name is required')
        
        if not data.get('mobile', '').strip():
            errors.append('Mobile number is required')
        elif len(data.get('mobile', '')) != 10 or not data.get('mobile', '').isdigit():
            errors.append('Mobile number must be 10 digits')
        
        if data.get('password') != data.get('confirmPassword'):
            errors.append('Passwords do not match')
        
        if len(data.get('password', '')) < 6:
            errors.append('Password must be at least 6 characters')
        
        # Validate Aadhar if provided
        aadhar = data.get('aadhar_number', '')
        if aadhar and len(aadhar) != 12:
            errors.append('Aadhar number must be 12 digits')
        
        if not data.get('state', '').strip():
            errors.append('State is required')
        
        if not data.get('district', '').strip():
            errors.append('District is required')
        
        if errors:
            print(f"✗ Validation failed: {', '.join(errors)}")
        else:
            print("✓ Validation passed")

if __name__ == "__main__":
    # Test backend registration
    backend_success = test_registration_flow()
    
    # Test frontend validation logic
    test_frontend_validation()
    
    print(f"\n=== SUMMARY ===")
    if backend_success:
        print("✓ Backend registration is working")
        print("✗ Issue is likely in frontend validation or state management")
    else:
        print("✗ Backend registration is failing")
        print("✗ Issue is in backend/API")