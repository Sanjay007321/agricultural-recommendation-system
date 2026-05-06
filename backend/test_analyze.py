import requests

BASE_URL = "http://127.0.0.1:8001/api"

def test_analysis():
    print("Registering user...")
    register_data = {
        "full_name": "Test User",
        "mobile": "6161616161",
        "password": "testpass",
        "state": "Tamil Nadu",
        "district": "Chennai"
    }
    # ignore if already registered
    res_reg = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print("Register response:", res_reg.status_code, res_reg.text)
    
    print("Logging in...")
    login_data = {
        "mobile": "6161616161",
        "password": "testpass"
    }
    login_res = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    if login_res.status_code != 200:
        print(f"Login failed: {login_res.text}")
        return
        
    token = login_res.json()["access_token"]
    
    print("Running analysis...")
    analysis_data = {
        "land_area_acres": 5.0,
        "soil_type": "Loamy",
        "soil_ph": 6.5,
        "nitrogen": 150,
        "phosphorus": 50,
        "potassium": 100,
        "state": "Tamil Nadu",
        "district": "Chennai",
        "season": "",
        "rainfall_mm": 800,
        "temperature_c": 28,
        "humidity_percent": 60,
        "budget_inr": 50000,
        "crop_preference": "auto",
        "crop_variety": "",
        "nearest_mandi": "",
        "sowing_date": ""
    }
    
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.post(f"{BASE_URL}/analyze", json=analysis_data, headers=headers)
    print(f"Status: {res.status_code}")
    if res.status_code != 200:
        print(f"Error: {res.text}")
    else:
        print("Success!")
        print(res.json())

if __name__ == "__main__":
    test_analysis()
