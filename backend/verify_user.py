import sqlite3

def verify_user():
    """Verify the newly created user with Aadhar"""
    conn = sqlite3.connect('crop.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT full_name, mobile, aadhar_number FROM users WHERE mobile='8888888888'")
    result = cursor.fetchone()
    
    if result:
        print(f'User created successfully:')
        print(f'  Name: {result[0]}')
        print(f'  Mobile: {result[1]}')
        print(f'  Aadhar: {result[2]}')
    else:
        print('User not found')
    
    conn.close()

if __name__ == "__main__":
    verify_user()