import sqlite3
import os

def add_aadhar_column():
    """Add aadhar_number column to users table"""
    
    # Database path - adjust this to match your setup
    db_path = "crop.db"
    
    # Check if database exists
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return False
    
    try:
        # Connect to database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if column already exists
        cursor.execute("PRAGMA table_info(users)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'aadhar_number' in columns:
            print("Column 'aadhar_number' already exists")
            conn.close()
            return True
        
        # Add the column (without UNIQUE constraint, we'll handle uniqueness in app logic)
        cursor.execute("ALTER TABLE users ADD COLUMN aadhar_number VARCHAR(12)")
        conn.commit()
        
        print("Successfully added 'aadhar_number' column to users table")
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error adding column: {e}")
        return False

if __name__ == "__main__":
    success = add_aadhar_column()
    if success:
        print("Migration completed successfully!")
    else:
        print("Migration failed!")