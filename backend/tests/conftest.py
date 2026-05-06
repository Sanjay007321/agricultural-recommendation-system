import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from app.database import Base, get_db
from app.models.user import User
from app.services.auth_service import get_password_hash

# Test database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_crop.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(test_db):
    def override_get_db():
        try:
            yield test_db
        finally:
            test_db.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(test_db):
    """Create a test user"""
    user_data = {
        "farmer_id": "TEST001",
        "full_name": "Test Farmer",
        "mobile": "9999999999",
        "password": "testpassword123",
        "state": "Maharashtra",
        "district": "Pune",
        "village": "Test Village",
        "land_size_acres": 5.5
    }
    
    password_hash = get_password_hash(user_data["password"])
    db_user = User(
        farmer_id=user_data["farmer_id"],
        full_name=user_data["full_name"],
        mobile=user_data["mobile"],
        password_hash=password_hash,
        state=user_data["state"],
        district=user_data["district"],
        village=user_data["village"],
        land_size_acres=user_data["land_size_acres"]
    )
    
    test_db.add(db_user)
    test_db.commit()
    test_db.refresh(db_user)
    
    # Add plain password for testing
    db_user.plain_password = user_data["password"]
    return db_user

@pytest.fixture(scope="function")
def auth_headers(client, test_user):
    """Get authentication headers for a test user"""
    response = client.post("/api/auth/login", json={
        "mobile": test_user.mobile,
        "password": test_user.plain_password
    })
    
    assert response.status_code == 200
    token_data = response.json()
    
    return {
        "Authorization": f"Bearer {token_data['access_token']}",
        "Content-Type": "application/json"
    }