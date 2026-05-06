import sqlite3

def check_users():
    """Check existing users in database"""
    conn = sqlite3.connect('crop.db')
    cursor = conn.cursor()
    
    # Check existing users
    cursor.execute('SELECT mobile, aadhar_number, full_name FROM users')
    results = cursor.fetchall()
    
    print('Existing users:')
    for row in results:
        print(f'Mobile: {row[0]}, Aadhar: {row[1]}, Name: {row[2]}')
    
    # Check table structure
    cursor.execute('PRAGMA table_info(users)')
    columns = cursor.fetchall()
    print('\nTable columns:')
    for col in columns:
        print(f'Column: {col[1]}, Type: {col[2]}, Not Null: {col[3]}, Default: {col[4]}, PK: {col[5]}')
    
    conn.close()

if __name__ == "__main__":
    check_users()