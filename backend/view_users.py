import sqlite3
from datetime import datetime

# Connect to the database
conn = sqlite3.connect('crop.db')
cursor = conn.cursor()

# Query all users
cursor.execute("""
    SELECT id, farmer_id, full_name, mobile, state, district, village, land_size_acres, created_at 
    FROM users 
    ORDER BY created_at DESC
""")

users = cursor.fetchall()

print("=" * 100)
print("REGISTERED USERS DATA")
print("=" * 100)
print(f"{'ID':<5} {'Farmer ID':<20} {'Name':<20} {'Mobile':<12} {'State':<15} {'District':<20} {'Registered'}")
print("-" * 100)

for user in users:
    user_id, farmer_id, full_name, mobile, state, district, village, land_size, created_at = user
    
    # Format the date
    try:
        reg_date = datetime.fromisoformat(created_at.replace('Z', '+00:00')).strftime('%Y-%m-%d %H:%M')
    except:
        reg_date = created_at[:19] if created_at else 'Unknown'
    
    print(f"{user_id:<5} {farmer_id:<20} {full_name:<20} {mobile:<12} {state:<15} {district:<20} {reg_date}")

print("=" * 100)
print(f"Total registered users: {len(users)}")
print("=" * 100)

# Show detailed info for each user
if users:
    print("\nDETAILED USER INFORMATION:")
    print("=" * 50)
    for user in users:
        user_id, farmer_id, full_name, mobile, state, district, village, land_size, created_at = user
        print(f"\nUser ID: {user_id}")
        print(f"Farmer ID: {farmer_id}")
        print(f"Full Name: {full_name}")
        print(f"Mobile: {mobile}")
        print(f"Location: {district}, {state}")
        if village:
            print(f"Village: {village}")
        if land_size:
            print(f"Land Size: {land_size} acres")
        print(f"Registration Date: {created_at}")

conn.close()