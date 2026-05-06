import sqlite3

def find_user_by_mobile(mobile_number):
    conn = sqlite3.connect('crop.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, farmer_id, full_name, mobile, state, district, village, land_size_acres, created_at 
        FROM users 
        WHERE mobile = ?
    """, (mobile_number,))
    
    user = cursor.fetchone()
    conn.close()
    
    if user:
        user_id, farmer_id, full_name, mobile, state, district, village, land_size, created_at = user
        print(f"User found!")
        print(f"=========")
        print(f"Farmer ID: {farmer_id}")
        print(f"Full Name: {full_name}")
        print(f"Mobile: {mobile}")
        print(f"Location: {district}, {state}")
        if village:
            print(f"Village: {village}")
        if land_size:
            print(f"Land Size: {land_size} acres")
        print(f"Registration Date: {created_at}")
        return True
    else:
        print(f"No user found with mobile number: {mobile_number}")
        return False

# Example usage - replace with your actual mobile number
if __name__ == "__main__":
    mobile_to_find = input("Enter mobile number to search: ")
    find_user_by_mobile(mobile_to_find)