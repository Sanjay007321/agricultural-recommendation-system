import sqlite3
import os
from datetime import datetime

def connect_to_database():
    """Connect to the SQLite database"""
    try:
        conn = sqlite3.connect('./crop.db')
        print("✅ Successfully connected to database")
        return conn
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return None

def get_database_info():
    """Get database schema and basic info"""
    conn = connect_to_database()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    
    print("\n📊 DATABASE SCHEMA")
    print("=" * 50)
    print("Tables in database:")
    for table in tables:
        print(f"  - {table[0]}")
        
        # Get table structure
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        print(f"    Columns:")
        for col in columns:
            print(f"      {col[1]} ({col[2]})")
    
    conn.close()

def query_users():
    """Query all users with formatted output"""
    conn = connect_to_database()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, farmer_id, full_name, mobile, state, district, 
               village, land_size_acres, created_at 
        FROM users 
        ORDER BY created_at DESC
    """)
    
    users = cursor.fetchall()
    
    print(f"\n👥 REGISTERED USERS ({len(users)} total)")
    print("=" * 100)
    print(f"{'ID':<3} {'Farmer ID':<18} {'Name':<15} {'Mobile':<12} {'State':<12} {'District':<15}")
    print("-" * 100)
    
    for user in users:
        user_id, farmer_id, full_name, mobile, state, district, village, land_size, created_at = user
        print(f"{user_id:<3} {farmer_id:<18} {full_name:<15} {mobile:<12} {state:<12} {district:<15}")
    
    conn.close()

def get_user_statistics():
    """Get statistics about users"""
    conn = connect_to_database()
    if not conn:
        return
    
    cursor = conn.cursor()
    
    # Total users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    # Users by state
    cursor.execute("""
        SELECT state, COUNT(*) as count 
        FROM users 
        GROUP BY state 
        ORDER BY count DESC
    """)
    users_by_state = cursor.fetchall()
    
    # Latest registration
    cursor.execute("""
        SELECT created_at 
        FROM users 
        ORDER BY created_at DESC 
        LIMIT 1
    """)
    latest_reg = cursor.fetchone()
    
    print(f"\n📈 STATISTICS")
    print("=" * 30)
    print(f"Total Users: {total_users}")
    if latest_reg:
        print(f"Latest Registration: {latest_reg[0][:19]}")
    
    print(f"\nUsers by State:")
    for state, count in users_by_state:
        print(f"  {state}: {count} users")
    
    conn.close()

if __name__ == "__main__":
    print("🌱 CROP MANAGEMENT SYSTEM - DATABASE CONNECTOR")
    print("=" * 50)
    
    get_database_info()
    query_users()
    get_user_statistics()
    
    print(f"\n📁 Database file location: {os.path.abspath('./crop.db')}")