import requests
import json

def test_district_api():
    """Test the district API directly"""
    try:
        print("Testing district API...")
        response = requests.get('http://localhost:8001/api/states')
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ API Response: {len(data)} states found")
            
            # Find Tamil Nadu
            tn = next((s for s in data if s['name'] == 'Tamil Nadu'), None)
            if tn:
                print(f"✅ Tamil Nadu found with {len(tn['districts'])} districts")
                print(f"✅ Erode available: {'Erode' in tn['districts']}")
                print(f"Sample districts: {tn['districts'][:5]}")
                
                # Test specific search
                erode_districts = [d for d in tn['districts'] if 'erode' in d.lower()]
                print(f"Districts matching 'erode': {erode_districts}")
            else:
                print("❌ Tamil Nadu not found in data")
                
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return False

def test_registration_flow():
    """Simulate the registration flow"""
    try:
        print("\nTesting registration flow...")
        
        # Step 1: Get states
        response = requests.get('http://localhost:8001/api/states')
        states = response.json()
        
        # Step 2: Select Tamil Nadu
        tn = next((s for s in states if s['name'] == 'Tamil Nadu'), None)
        if not tn:
            print("❌ Tamil Nadu not found")
            return False
            
        print(f"✅ Selected Tamil Nadu with {len(tn['districts'])} districts")
        
        # Step 3: Verify Erode exists
        districts = tn['districts']
        if 'Erode' not in districts:
            print("❌ Erode not found in Tamil Nadu districts")
            return False
            
        print("✅ Erode found in districts")
        
        # Step 4: Test district search
        search_results = [d for d in districts if 'erode' in d.lower()]
        print(f"✅ Search results for 'erode': {search_results}")
        
        return True
        
    except Exception as e:
        print(f"❌ Registration flow test failed: {e}")
        return False

if __name__ == "__main__":
    print("DISTRICT FUNCTIONALITY TEST")
    print("=" * 30)
    
    api_test = test_district_api()
    flow_test = test_registration_flow()
    
    if api_test and flow_test:
        print("\n🎉 ALL TESTS PASSED - District system is working!")
        print("✅ Users should be able to select Erode in registration")
    else:
        print("\n💥 SOME TESTS FAILED - District system needs attention")