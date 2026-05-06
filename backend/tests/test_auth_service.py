import pytest
from unittest.mock import Mock, patch
from sqlalchemy.orm import Session
from app.services.auth_service import (
    create_user, authenticate_user, create_access_token,
    create_refresh_token, get_current_user, verify_token,
    get_user_by_id, get_password_hash, verify_password
)
from app.models.schemas import UserRegister
from app.models.user import User

class TestAuthService:
    """Test authentication service functions"""
    
    @pytest.fixture
    def mock_db(self):
        return Mock(spec=Session)
    
    @pytest.fixture
    def user_data(self):
        return UserRegister(
            full_name="Test User",
            mobile="9999999999",
            password="testpassword123",
            state="Maharashtra",
            district="Pune",
            village="Test Village",
            land_size_acres=5.5
        )
    
    def test_create_user_success(self, mock_db, user_data):
        """Test successful user creation"""
        with patch('app.services.auth_service.generate_farmer_id') as mock_gen_id:
            mock_gen_id.return_value = "FM001"
            
            # Mock db query to return None (no existing user)
            mock_db.query.return_value.filter.return_value.first.return_value = None
            
            result = create_user(mock_db, user_data)
            
            assert isinstance(result, User)
            assert result.farmer_id == "FM001"
            assert result.full_name == user_data.full_name
            assert result.mobile == user_data.mobile
            assert result.state == user_data.state
            assert result.district == user_data.district
            
            # Verify db operations were called
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()
    
    def test_create_user_duplicate_mobile(self, mock_db, user_data):
        """Test user creation with duplicate mobile"""
        # Mock existing user
        existing_user = User(mobile=user_data.mobile)
        mock_db.query.return_value.filter.return_value.first.return_value = existing_user
        
        with pytest.raises(Exception):  # Should raise some exception
            create_user(mock_db, user_data)
    
    def test_authenticate_user_success(self, mock_db, user_data):
        """Test successful user authentication"""
        # Create a mock user with password hash
        password_hash = get_password_hash(user_data.password)
        mock_user = User(
            id=1,
            farmer_id="FM001",
            mobile=user_data.mobile,
            password_hash=password_hash
        )
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        result = authenticate_user(mock_db, user_data.mobile, user_data.password)
        
        assert result is not None
        assert result.id == 1
        assert result.mobile == user_data.mobile
    
    def test_authenticate_user_invalid_password(self, mock_db):
        """Test authentication with invalid password"""
        mobile = "9999999999"
        password = "wrongpassword"
        
        # Create a mock user with different password
        password_hash = get_password_hash("correctpassword")
        mock_user = User(mobile=mobile, password_hash=password_hash)
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_user
        
        result = authenticate_user(mock_db, mobile, password)
        assert result is None
    
    def test_authenticate_user_nonexistent(self, mock_db):
        """Test authentication for non-existent user"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = authenticate_user(mock_db, "9999999999", "anypassword")
        assert result is None
    
    def test_create_access_token(self):
        """Test JWT access token creation"""
        data = {"sub": "1", "farmer_id": "FM001"}
        
        token = create_access_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        # Token should contain JWT structure (header.payload.signature)
        parts = token.split('.')
        assert len(parts) == 3
    
    def test_create_refresh_token(self):
        """Test JWT refresh token creation"""
        data = {"sub": "1", "farmer_id": "FM001"}
        
        token = create_refresh_token(data)
        
        assert isinstance(token, str)
        assert len(token) > 0
        parts = token.split('.')
        assert len(parts) == 3
    
    def test_verify_token_valid(self):
        """Test valid token verification"""
        data = {"sub": "1", "farmer_id": "FM001"}
        token = create_access_token(data)
        
        verified_data = verify_token(token, "access")
        
        assert verified_data is not None
        assert str(verified_data.user_id) == "1"
        assert verified_data.farmer_id == "FM001"
    
    def test_verify_token_invalid(self):
        """Test invalid token verification"""
        invalid_token = "invalid.token.string"
        
        verified_data = verify_token(invalid_token, "access")
        assert verified_data is None
    
    def test_verify_token_expired(self):
        """Test expired token verification"""
        # Create token with very short expiration
        from datetime import timedelta
        from jose import jwt
        from app.config import settings
        
        data = {"sub": "1", "exp": 0}  # Expired timestamp
        expired_token = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        verified_data = verify_token(expired_token, "access")
        assert verified_data is None
    
    def test_get_password_hash(self):
        """Test password hashing"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        assert isinstance(hashed, str)
        assert len(hashed) > 0
        assert hashed != password  # Should be different from original
    
    def test_verify_password_correct(self):
        """Test correct password verification"""
        password = "testpassword123"
        hashed = get_password_hash(password)
        
        result = verify_password(password, hashed)
        assert result is True
    
    def test_verify_password_incorrect(self):
        """Test incorrect password verification"""
        password = "testpassword123"
        wrong_password = "wrongpassword"
        hashed = get_password_hash(password)
        
        result = verify_password(wrong_password, hashed)
        assert result is False
    
    def test_get_user_by_id_found(self, mock_db):
        """Test getting user by existing ID"""
        user_id = 1
        expected_user = User(id=user_id, farmer_id="FM001")
        
        mock_db.query.return_value.filter.return_value.first.return_value = expected_user
        
        result = get_user_by_id(mock_db, user_id)
        
        assert result == expected_user
        assert result.id == user_id
    
    def test_get_user_by_id_not_found(self, mock_db):
        """Test getting user by non-existent ID"""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = get_user_by_id(mock_db, 999)
        assert result is None