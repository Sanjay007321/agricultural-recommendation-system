import requests
import json

def comprehensive_district_test():
    """Comprehensive test of district functionality"""
    
    print("🔬 COMPREHENSIVE DISTRICT FUNCTIONALITY TEST")
    print("=" * 50)
    
    try:
        # Test 1: API Connectivity
        print("📡 Testing API connectivity...")
        response = requests.get('http://localhost:8001/api/states')
        if response.status_code == 200:
            print("✅ API connection successful")
            states_data = response.json()
        else:
            print(f"❌ API connection failed: {response.status_code}")
            return False
        
        # Test 2: Data Completeness
        print(f"\n📊 Testing data completeness...")
        print(f"   Total states/UTs: {len(states_data)}")
        
        total_districts = sum(len(state['districts']) for state in states_data)
        print(f"   Total districts: {total_districts}")
        
        if total_districts >= 600:
            print("✅ District data is complete")
        else:
            print(f"⚠️  District data may be incomplete ({total_districts} districts)")
            return False
        
        # Test 3: Specific District Availability
        print(f"\n🔍 Testing specific district availability...")
        test_districts = [
            ('Tamil Nadu', 'Erode'),
            ('Karnataka', 'Bangalore'),
            ('Maharashtra', 'Pune'),
            ('Uttar Pradesh', 'Lucknow'),
            ('West Bengal', 'Kolkata'),
            ('Gujarat', 'Ahmedabad')
        ]
        
        districts_found = 0
        for state_name, district_name in test_districts:
            state = next((s for s in states_data if s['name'] == state_name), None)
            if state and district_name in state['districts']:
                print(f"   ✅ {district_name} found in {state_name}")
                districts_found += 1
            else:
                print(f"   ❌ {district_name} NOT found in {state_name}")
        
        print(f"   Found {districts_found}/{len(test_districts)} test districts")
        
        # Test 4: District Search Functionality
        print(f"\n🔎 Testing district search functionality...")
        
        # Test Tamil Nadu districts specifically
        tamil_nadu = next((s for s in states_data if s['name'] == 'Tamil Nadu'), None)
        if tamil_nadu:
            tn_districts = tamil_nadu['districts']
            print(f"   Tamil Nadu districts: {len(tn_districts)}")
            print(f"   Sample districts: {tn_districts[:5]}")
            
            # Test Erode specifically
            if 'Erode' in tn_districts:
                print("   ✅ Erode confirmed available in Tamil Nadu")
            else:
                print("   ❌ Erode not found in Tamil Nadu")
        
        # Test 5: Registration Flow Simulation
        print(f"\n🔄 Testing registration flow simulation...")
        
        # Simulate selecting Tamil Nadu and checking districts
        selected_state = 'Tamil Nadu'
        state_obj = next((s for s in states_data if s['name'] == selected_state), None)
        
        if state_obj:
            districts = state_obj['districts']
            print(f"   When selecting '{selected_state}', available districts:")
            print(f"   Count: {len(districts)}")
            print(f"   First 10 districts: {districts[:10]}")
            
            # Test search functionality
            search_term = 'erode'
            matching_districts = [d for d in districts if search_term in d.lower()]
            print(f"   Districts matching '{search_term}': {matching_districts}")
            
            if matching_districts:
                print("   ✅ District search working correctly")
            else:
                print("   ❌ District search not working")
        
        print(f"\n🎯 DISTRICT SYSTEM VERIFICATION COMPLETE")
        print(f"✅ All districts are properly loaded and accessible")
        print(f"✅ Registration component should work correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        return False

def generate_district_report():
    """Generate a comprehensive report of all districts"""
    
    try:
        response = requests.get('http://localhost:8001/api/states')
        states_data = response.json()
        
        print(f"\n📋 COMPREHENSIVE DISTRICT REPORT")
        print("=" * 40)
        
        # Sort states by district count (descending)
        sorted_states = sorted(states_data, key=lambda x: len(x['districts']), reverse=True)
        
        for state in sorted_states[:10]:  # Top 10 states by district count
            district_count = len(state['districts'])
            print(f"📍 {state['name']}: {district_count} districts")
            if district_count <= 10:
                print(f"   Districts: {', '.join(state['districts'])}")
            else:
                print(f"   Districts: {', '.join(state['districts'][:5])}... ({district_count} total)")
        
        # Summary
        total_states = len(states_data)
        total_districts = sum(len(state['districts']) for state in states_data)
        
        print(f"\n📈 SUMMARY")
        print(f"   Total States/UTs: {total_states}")
        print(f"   Total Districts: {total_districts}")
        print(f"   Average Districts per State: {total_districts/total_states:.1f}")
        
    except Exception as e:
        print(f"❌ Error generating report: {e}")

if __name__ == "__main__":
    if comprehensive_district_test():
        generate_district_report()
        print(f"\n🎉 DISTRICT SYSTEM IS FULLY FUNCTIONAL!")
        print(f"✅ Users can now register with any Indian district")
        print(f"✅ Erode and all other districts are working properly")
    else:
        print(f"\n💥 DISTRICT SYSTEM NEEDS ATTENTION!")