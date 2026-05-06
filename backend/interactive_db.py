import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path='./crop.db'):
        self.db_path = db_path
        self.conn = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path)
            print(f"✅ Connected to database: {os.path.abspath(self.db_path)}")
            return True
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
            print("🔌 Disconnected from database")
    
    def execute_query(self, query, params=None):
        """Execute a query and return results"""
        if not self.conn:
            print("❌ No database connection")
            return None
            
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return cursor.fetchall()
            else:
                self.conn.commit()
                return cursor.rowcount
        except Exception as e:
            print(f"❌ Query execution failed: {e}")
            return None
    
    def get_table_info(self, table_name):
        """Get detailed information about a table"""
        query = f"PRAGMA table_info({table_name})"
        return self.execute_query(query)
    
    def list_tables(self):
        """List all tables in database"""
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        return self.execute_query(query)
    
    def search_user(self, search_term):
        """Search users by name, mobile, or farmer_id"""
        query = """
            SELECT id, farmer_id, full_name, mobile, state, district, created_at
            FROM users 
            WHERE full_name LIKE ? OR mobile LIKE ? OR farmer_id LIKE ?
            ORDER BY created_at DESC
        """
        search_pattern = f"%{search_term}%"
        return self.execute_query(query, (search_pattern, search_pattern, search_pattern))
    
    def delete_user(self, user_id):
        """Delete a user by ID (be careful!)"""
        # First check if user exists
        check_query = "SELECT full_name FROM users WHERE id = ?"
        user = self.execute_query(check_query, (user_id,))
        
        if not user:
            print(f"❌ User with ID {user_id} not found")
            return False
        
        print(f"⚠️  About to delete user: {user[0][0]} (ID: {user_id})")
        confirm = input("Type 'DELETE' to confirm: ")
        
        if confirm == 'DELETE':
            delete_query = "DELETE FROM users WHERE id = ?"
            result = self.execute_query(delete_query, (user_id,))
            if result:
                print(f"✅ User deleted successfully")
                return True
        else:
            print("❌ Deletion cancelled")
            return False
    
    def export_users_csv(self, filename='users_export.csv'):
        """Export users to CSV format"""
        query = """
            SELECT id, farmer_id, full_name, mobile, state, district, 
                   village, land_size_acres, created_at
            FROM users 
            ORDER BY created_at DESC
        """
        users = self.execute_query(query)
        
        if not users:
            print("❌ No users to export")
            return False
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                # Write header
                f.write("ID,Farmer_ID,Full_Name,Mobile,State,District,Village,Land_Size,Created_At\n")
                
                # Write data
                for user in users:
                    line = ','.join([str(field) if field is not None else '' for field in user])
                    f.write(line + '\n')
            
            print(f"✅ Exported {len(users)} users to {filename}")
            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False

def main_menu():
    """Interactive menu system"""
    db = DatabaseManager()
    
    if not db.connect():
        return
    
    while True:
        print("\n" + "="*50)
        print("🌱 CROP MANAGEMENT SYSTEM - DATABASE MANAGER")
        print("="*50)
        print("1. View Database Schema")
        print("2. List All Users")
        print("3. Search Users")
        print("4. View Statistics")
        print("5. Export Users to CSV")
        print("6. Delete User (Careful!)")
        print("7. Run Custom Query")
        print("0. Exit")
        print("="*50)
        
        choice = input("Enter your choice: ").strip()
        
        if choice == '1':
            tables = db.list_tables()
            if tables:
                print("\n📋 TABLES:")
                for table in tables:
                    print(f"\nTable: {table[0]}")
                    columns = db.get_table_info(table[0])
                    for col in columns:
                        print(f"  {col[1]} ({col[2]})")
        
        elif choice == '2':
            users = db.execute_query("""
                SELECT id, farmer_id, full_name, mobile, state, district, created_at 
                FROM users 
                ORDER BY created_at DESC
            """)
            if users:
                print(f"\n👥 ALL USERS ({len(users)}):")
                print("-" * 80)
                for user in users:
                    print(f"ID:{user[0]} | {user[1]} | {user[2]} | {user[3]} | {user[4]}, {user[5]} | {user[6][:19]}")
        
        elif choice == '3':
            search_term = input("Enter search term (name/mobile/farmer_id): ")
            results = db.search_user(search_term)
            if results:
                print(f"\n🔍 SEARCH RESULTS ({len(results)}):")
                for user in results:
                    print(f"ID:{user[0]} | {user[1]} | {user[2]} | {user[3]} | {user[4]}, {user[5]}")
            else:
                print("No users found")
        
        elif choice == '4':
            # Statistics
            total = db.execute_query("SELECT COUNT(*) FROM users")[0][0]
            by_state = db.execute_query("SELECT state, COUNT(*) FROM users GROUP BY state")
            
            print(f"\n📈 STATISTICS:")
            print(f"Total Users: {total}")
            print("By State:")
            for state, count in by_state:
                print(f"  {state}: {count}")
        
        elif choice == '5':
            filename = input("Enter filename (default: users_export.csv): ").strip()
            if not filename:
                filename = 'users_export.csv'
            db.export_users_csv(filename)
        
        elif choice == '6':
            try:
                user_id = int(input("Enter User ID to delete: "))
                db.delete_user(user_id)
            except ValueError:
                print("❌ Invalid ID")
        
        elif choice == '7':
            query = input("Enter SQL query: ")
            results = db.execute_query(query)
            if results:
                print("Results:")
                for row in results:
                    print(row)
            elif results == 0:
                print("Query executed successfully (no results)")
        
        elif choice == '0':
            break
        
        else:
            print("❌ Invalid choice")
    
    db.disconnect()
    print("👋 Goodbye!")

if __name__ == "__main__":
    main_menu()