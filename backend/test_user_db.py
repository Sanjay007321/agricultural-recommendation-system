import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.user import User
from app.models.schemas import UserResponse
import json

def test_user_query():
    # Create a database session
    db = SessionLocal()
    
    try:
        # Try to get a user
        user = db.query(User).first()
        if user:
            print(f"Found user: {user.full_name}")
            print(f"User ID: {user.id}")
            print(f"Aadhar number: {user.aadhar_number}")
            print(f"User attributes: {vars(user)}")
            
            # Try to create UserResponse
            try:
                primary_crops = None
                if user.primary_crops:
                    try:
                        primary_crops = json.loads(user.primary_crops)
                    except Exception as e:
                        print(f"Error parsing primary_crops: {e}")
                        primary_crops = None
                
                print(f"Creating UserResponse with aadhar_number: {user.aadhar_number}")
                
                response = UserResponse(
                    id=user.id,
                    farmer_id=user.farmer_id,
                    full_name=user.full_name,
                    mobile=user.mobile,
                    aadhar_number=user.aadhar_number,
                    state=user.state,
                    district=user.district,
                    village=user.village,
                    land_size_acres=user.land_size_acres,
                    primary_crops=primary_crops,
                    created_at=user.created_at
                )
                
                print(f"UserResponse created successfully: {response}")
                print(f"UserResponse dict: {response.dict()}")
                
            except Exception as e:
                print(f"Error creating UserResponse: {e}")
                import traceback
                traceback.print_exc()
        else:
            print("No users found in database")
            
    except Exception as e:
        print(f"Database error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    test_user_query()