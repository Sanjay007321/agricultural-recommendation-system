from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import json

from app.database import get_db
from app.models.schemas import (
    UserRegister, UserLogin, UserResponse, Token, ProfileUpdate
)
from app.services.auth_service import (
    create_user, authenticate_user, create_access_token, 
    create_refresh_token, get_current_user, verify_token,
    get_user_by_id
)
from app.models.user import User

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/register", response_model=Token)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new farmer and return JWT tokens"""
    user = create_user(db, user_data)
    
    access_token = create_access_token(
        data={"sub": str(user.id), "farmer_id": user.farmer_id}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "farmer_id": user.farmer_id}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        farmer_id=user.farmer_id
    )

@router.post("/login", response_model=Token)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """Login with mobile and password"""
    user = authenticate_user(db, user_data.mobile, user_data.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid mobile number or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": str(user.id), "farmer_id": user.farmer_id}
    )
    refresh_token = create_refresh_token(
        data={"sub": str(user.id), "farmer_id": user.farmer_id}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        farmer_id=user.farmer_id
    )

@router.post("/refresh", response_model=Token)
def refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    """Get new access token using refresh token"""
    token_data = verify_token(refresh_token, "refresh")
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user = get_user_by_id(db, token_data.user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    new_access_token = create_access_token(
        data={"sub": user.id, "farmer_id": user.farmer_id}
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user.id, "farmer_id": user.farmer_id}
    )
    
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token,
        farmer_id=user.farmer_id
    )

@router.get("/me", response_model=UserResponse)
def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current logged in user's profile"""
    try:
        # Simple response without complex processing
        return UserResponse(
            id=current_user.id,
            farmer_id=current_user.farmer_id,
            full_name=current_user.full_name,
            mobile=current_user.mobile,
            aadhar_number=current_user.aadhar_number,
            state=current_user.state,
            district=current_user.district,
            village=current_user.village,
            land_size_acres=current_user.land_size_acres,
            primary_crops=[],  # Simplified for testing
            created_at=current_user.created_at
        )
    except Exception as e:
        print(f"Error in get_current_user_info: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/profile", response_model=UserResponse)
def update_profile(
    profile_data: ProfileUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update farmer profile"""
    if profile_data.full_name is not None and profile_data.full_name.strip():
        current_user.full_name = profile_data.full_name.strip()
    if profile_data.village is not None:
        current_user.village = profile_data.village
    if profile_data.land_size_acres is not None:
        current_user.land_size_acres = profile_data.land_size_acres
    if profile_data.primary_crops is not None:
        current_user.primary_crops = json.dumps(profile_data.primary_crops)
    
    db.commit()
    db.refresh(current_user)
    
    crops = None
    if current_user.primary_crops:
        try:
            crops = json.loads(current_user.primary_crops)
        except:
            crops = None
    
    return UserResponse(
        id=current_user.id,
        farmer_id=current_user.farmer_id,
        full_name=current_user.full_name,
        mobile=current_user.mobile,
        aadhar_number=current_user.aadhar_number,
        state=current_user.state,
        district=current_user.district,
        village=current_user.village,
        land_size_acres=current_user.land_size_acres,
        primary_crops=crops,
        created_at=current_user.created_at
    )
