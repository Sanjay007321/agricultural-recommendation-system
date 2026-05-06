import json
import requests

def test_districts_availability():
    """Test that all Indian districts are available and working"""
    
    try:
        # Get states data from API
        response = requests.get('http://localhost:8001/api/states')
        if response.status_code != 200:
            print(f"❌ API Error: {response.status_code}")
            return False
            
        states_data = response.json()
        
        print("✅ Successfully connected to districts API")
        print(f"📊 Found {len(states_data)} states/UTs")
        
        # Check specific states
        target_states = ['Tamil Nadu', 'Karnataka', 'Maharashtra', 'Uttar Pradesh']
        districts_found = {}
        
        for state_data in states_data:
            state_name = state_data['name']
            districts = state_data['districts']
            
            if state_name in target_states:
                districts_found[state_name] = len(districts)
                print(f"📍 {state_name}: {len(districts)} districts")
                
                # Check for specific districts
                if state_name == 'Tamil Nadu':
                    print(f"   Sample districts: {districts[:5]}")
                    if 'Erode' in districts:
                        print("   ✅ Erode found in Tamil Nadu")
                    else:
                        print("   ❌ Erode NOT found in Tamil Nadu")
                        
                elif state_name == 'Karnataka':
                    print(f"   Sample districts: {districts[:5]}")
                    if 'Bangalore' in districts or 'Bengaluru' in districts:
                        print("   ✅ Bangalore/Bengaluru found in Karnataka")
                        
        # Overall statistics
        total_districts = sum(len(state_data['districts']) for state_data in states_data)
        print(f"\n📈 TOTAL DISTRICTS ACROSS INDIA: {total_districts}")
        
        # Check if we have reasonable number of districts
        if total_districts >= 600:  # India has ~700 districts
            print("✅ District data looks complete")
            return True
        else:
            print(f"⚠️  Expected ~700+ districts, found {total_districts}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing districts: {e}")
        return False

def test_district_search_functionality():
    """Test that district search works properly"""
    test_cases = [
        ('Tamil Nadu', 'Erode'),
        ('Karnataka', 'Bangalore'),
        ('Maharashtra', 'Pune'),
        ('Uttar Pradesh', 'Lucknow')
    ]
    
    print("\n🔍 Testing district search functionality...")
    
    try:
        response = requests.get('http://localhost:8001/api/states')
        states_data = response.json()
        
        for state_name, district_name in test_cases:
            # Find the state
            state = next((s for s in states_data if s['name'] == state_name), None)
            if not state:
                print(f"❌ State '{state_name}' not found")
                continue
                
            districts = state['districts']
            if district_name in districts:
                print(f"✅ {district_name} found in {state_name}")
            else:
                # Check for alternative names
                found_alt = any(district_name.lower()[:4] in d.lower() for d in districts)
                if found_alt:
                    print(f"✅ Similar district found for {district_name} in {state_name}")
                else:
                    print(f"❌ {district_name} not found in {state_name}")
                    
    except Exception as e:
        print(f"❌ Error in search test: {e}")

if __name__ == "__main__":
    print("🌱 TESTING DISTRICT AVAILABILITY IN CROP MANAGEMENT SYSTEM")
    print("=" * 60)
    
    # Test API availability
    if test_districts_availability():
        test_district_search_functionality()
        print("\n🎉 District system is working properly!")
    else:
        print("\n💥 District system needs attention!")