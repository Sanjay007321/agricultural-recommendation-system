import json

def validate_district_dataset():
    """Validate and enhance the district dataset"""
    
    # Read the current districts data
    with open('app/data/states_districts.json', 'r', encoding='utf-8') as f:
        states_districts = json.load(f)
    
    print("📊 DISTRICT DATASET VALIDATION")
    print("=" * 40)
    
    total_districts = 0
    issues_found = []
    
    # Validate each state
    for state_name, districts in states_districts.items():
        district_count = len(districts)
        total_districts += district_count
        
        print(f"📍 {state_name}: {district_count} districts")
        
        # Check for common issues
        for i, district in enumerate(districts):
            # Check for duplicates
            if districts.count(district) > 1:
                issues_found.append(f"Duplicate district '{district}' in {state_name}")
            
            # Check for empty or invalid names
            if not district or len(district.strip()) < 2:
                issues_found.append(f"Invalid district name in {state_name}: '{district}'")
            
            # Check for special characters that might cause issues
            if any(char in district for char in ['"', "'", '\\']):
                issues_found.append(f"Special characters in district name '{district}' in {state_name}")
    
    print(f"\n📈 TOTAL DISTRICTS: {total_districts}")
    print(f"📊 STATES/UTs: {len(states_districts)}")
    
    # Report issues
    if issues_found:
        print(f"\n⚠️  ISSUES FOUND ({len(issues_found)}):")
        for issue in issues_found[:10]:  # Show first 10 issues
            print(f"   • {issue}")
        if len(issues_found) > 10:
            print(f"   ... and {len(issues_found) - 10} more issues")
    else:
        print("✅ No issues found in district dataset!")
    
    # Enhancement suggestions
    print(f"\n💡 ENHANCEMENT SUGGESTIONS:")
    print("   • Add alternate spellings for major cities")
    print("   • Include commonly used abbreviations")
    print("   • Add regional language variations")
    
    return len(issues_found) == 0

def enhance_district_data():
    """Enhance district data with common variations"""
    
    # Common district variations to add
    district_variations = {
        'Karnataka': {
            'Bangalore': ['Bengaluru', 'Bangalore Urban', 'Bangalore Rural'],
            'Belagavi': ['Belgaum']
        },
        'Tamil Nadu': {
            'Chennai': ['Madras'],
            'Coimbatore': ['Kovai']
        },
        'Maharashtra': {
            'Mumbai': ['Bombay'],
            'Pune': ['Poona']
        }
    }
    
    print("🔧 ENHANCING DISTRICT DATA WITH COMMON VARIATIONS")
    print("=" * 50)
    
    # Read current data
    try:
        with open('app/data/states_districts.json', 'r', encoding='utf-8') as f:
            states_districts = json.load(f)
    except FileNotFoundError:
        print("❌ District data file not found")
        return False
    
    # Add variations
    for state, variations in district_variations.items():
        if state in states_districts:
            original_count = len(states_districts[state])
            for district, alternatives in variations.items():
                if district in states_districts[state]:
                    # Add alternatives that don't already exist
                    for alt in alternatives:
                        if alt not in states_districts[state]:
                            states_districts[state].append(alt)
            
            new_count = len(states_districts[state])
            print(f"📍 {state}: {original_count} → {new_count} districts (+{new_count-original_count})")
    
    # Save enhanced data
    try:
        with open('app/data/states_districts_enhanced.json', 'w', encoding='utf-8') as f:
            json.dump(states_districts, f, indent=2, ensure_ascii=False)
        print("✅ Enhanced district data saved to states_districts_enhanced.json")
        return True
    except Exception as e:
        print(f"❌ Error saving enhanced data: {e}")
        return False

if __name__ == "__main__":
    # Validate current dataset
    is_valid = validate_district_dataset()
    
    print("\n" + "="*50)
    
    # Enhance dataset if needed
    if not is_valid or input("\nWould you like to enhance the district data? (y/n): ").lower() == 'y':
        enhance_district_data()
    
    print("\n🎯 DISTRICT SYSTEM OPTIMIZATION COMPLETE!")