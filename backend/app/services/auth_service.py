from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import bcrypt
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import settings
from app.models.user import User
from app.models.schemas import UserRegister, TokenData
from app.database import get_db
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def generate_farmer_id(state: str, db: Session) -> str:
    """Generate unique Farmer ID: KR-{STATE_CODE}-{YEAR}-{SEQUENCE}"""
    state_code = settings.STATE_CODES.get(state, "XX")
    year = datetime.now().year
    
    # Get the last sequence number for this state and year
    last_user = db.query(User).filter(
        User.farmer_id.like(f"KR-{state_code}-{year}-%")
    ).order_by(User.id.desc()).first()
    
    if last_user:
        last_sequence = int(last_user.farmer_id.split("-")[-1])
        new_sequence = last_sequence + 1
    else:
        new_sequence = 1
    
    return f"KR-{state_code}-{year}-{str(new_sequence).zfill(5)}"

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire, "type": "access"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire, "type": "refresh"})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def verify_token(token: str, token_type: str = "access") -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != token_type:
            return None
        user_id: int = payload.get("sub")
        farmer_id: str = payload.get("farmer_id")
        if user_id is None:
            return None
        return TokenData(user_id=user_id, farmer_id=farmer_id)
    except JWTError:
        return None

def get_user_by_mobile(db: Session, mobile: str) -> Optional[User]:
    return db.query(User).filter(User.mobile == mobile).first()

def get_user_by_farmer_id(db: Session, farmer_id: str) -> Optional[User]:
    return db.query(User).filter(User.farmer_id == farmer_id).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user_data: UserRegister) -> User:
    # Check if mobile already exists
    if get_user_by_mobile(db, user_data.mobile):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Mobile number already registered"
        )
    
    # Validate state and district against available states
    # Import here to avoid circular imports
    from app.api.analysis import get_states
    import json
    
    # Get available states and districts
    states_data = get_states()
    available_states = {state['name'] for state in states_data}
    
    if user_data.state not in available_states:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid state selected"
        )
    
    # Find the district list for the selected state
    selected_state_data = next((state for state in states_data if state['name'] == user_data.state), None)
    if selected_state_data and user_data.district not in selected_state_data['districts']:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid district for the selected state"
        )
    
    # Generate unique Farmer ID
    farmer_id = generate_farmer_id(user_data.state, db)
    
    # Check if Aadhar already exists
    if user_data.aadhar_number:
        existing_user = db.query(User).filter(User.aadhar_number == user_data.aadhar_number).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Aadhar number already registered"
            )
    
    # Create user
    db_user = User(
        farmer_id=farmer_id,
        full_name=user_data.full_name,
        mobile=user_data.mobile,
        aadhar_number=user_data.aadhar_number,
        password_hash=get_password_hash(user_data.password),
        state=user_data.state,
        district=user_data.district,
        village=user_data.village,
        land_size_acres=user_data.land_size_acres,
        primary_crops=json.dumps(user_data.primary_crops) if user_data.primary_crops else None
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, mobile: str, password: str) -> Optional[User]:
    user = get_user_by_mobile(db, mobile)
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    import sys
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    print(f"Token received: {token[:20]}...", flush=True)
    sys.stdout.flush()
    
    token_data = verify_token(token, "access")
    print(f"Token data: {token_data}", flush=True)
    sys.stdout.flush()
    
    if token_data is None:
        print("Token verification failed", flush=True)
        sys.stdout.flush()
        raise credentials_exception
    
    print(f"Looking for user with ID: {token_data.user_id}", flush=True)
    sys.stdout.flush()
    user = get_user_by_id(db, token_data.user_id)
    print(f"User found: {user}", flush=True)
    sys.stdout.flush()
    
    if user is None:
        print("User not found in database", flush=True)
        sys.stdout.flush()
        raise credentials_exception
    
    print(f"Returning user: {user.full_name}", flush=True)
    sys.stdout.flush()
    return user
