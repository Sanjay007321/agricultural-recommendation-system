import pytest
from fastapi.testclient import TestClient

class TestAuthAPI:
    """Test authentication endpoints"""
    
    def test_health_check(self, client: TestClient):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"
    
    def test_root_endpoint(self, client: TestClient):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_register_user_success(self, client: TestClient):
        """Test successful user registration"""
        user_data = {
            "full_name": "John Doe",
            "mobile": "8888888888",
            "password": "securepassword123",
            "state": "Maharashtra",
            "district": "Mumbai",
            "village": "Test Village",
            "land_size_acres": 10.5
        }
        
        response = client.post("/api/auth/register", json=user_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "farmer_id" in data
        assert data["farmer_id"].startswith("KR-")
    
    def test_register_user_missing_fields(self, client: TestClient):
        """Test registration with missing required fields"""
        incomplete_data = {
            "full_name": "John Doe",
            "mobile": "8888888888"
            # Missing password, state, district, etc.
        }
        
        response = client.post("/api/auth/register", json=incomplete_data)
        assert response.status_code == 422  # Validation error
    
    def test_register_duplicate_mobile(self, client: TestClient, test_user):
        """Test registration with duplicate mobile number"""
        user_data = {
            "full_name": "Another User",
            "mobile": test_user.mobile,  # Same mobile as existing user
            "password": "anotherpassword123",
            "state": "Karnataka",
            "district": "Bangalore",
            "village": "Test Village 2",
            "land_size_acres": 8.0
        }
        
        response = client.post("/api/auth/register", json=user_data)
        # Should either fail or handle gracefully
        assert response.status_code in [400, 409, 422]
    
    def test_login_success(self, client: TestClient, test_user):
        """Test successful login"""
        login_data = {
            "mobile": test_user.mobile,
            "password": test_user.plain_password
        }
        
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert "farmer_id" in data
    
    def test_login_invalid_credentials(self, client: TestClient):
        """Test login with invalid credentials"""
        login_data = {
            "mobile": "9999999999",
            "password": "wrongpassword"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_login_nonexistent_user(self, client: TestClient):
        """Test login with non-existent user"""
        login_data = {
            "mobile": "1111111111",
            "password": "anypassword"
        }
        
        response = client.post("/api/auth/login", json=login_data)
        assert response.status_code == 401
    
    def test_get_current_user_authenticated(self, client: TestClient, auth_headers):
        """Test getting current user info with valid token"""
        response = client.get("/api/auth/me", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "id" in data
        assert "farmer_id" in data
        assert "full_name" in data
        assert "mobile" in data
    
    def test_get_current_user_unauthenticated(self, client: TestClient):
        """Test getting current user info without token"""
        response = client.get("/api/auth/me")
        assert response.status_code == 401
    
    def test_get_current_user_invalid_token(self, client: TestClient):
        """Test getting current user info with invalid token"""
        headers = {"Authorization": "Bearer invalid.token.here"}
        response = client.get("/api/auth/me", headers=headers)
        assert response.status_code == 401
    
    def test_update_profile_success(self, client: TestClient, auth_headers):
        """Test successful profile update"""
        update_data = {
            "village": "Updated Village",
            "land_size_acres": 7.5,
            "primary_crops": ["Rice", "Wheat"]
        }
        
        response = client.put("/api/auth/profile", params=update_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["village"] == "Updated Village"
        assert data["land_size_acres"] == 7.5
        assert data["primary_crops"] == ["Rice", "Wheat"]
    
    def test_update_profile_partial_fields(self, client: TestClient, auth_headers):
        """Test partial profile update"""
        update_data = {
            "village": "Partially Updated Village"
            # Only update village, leave other fields unchanged
        }
        
        response = client.put("/api/auth/profile", params=update_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["village"] == "Partially Updated Village"
    
    def test_update_profile_unauthenticated(self, client: TestClient):
        """Test profile update without authentication"""
        update_data = {"village": "Unauthorized Update"}
        response = client.put("/api/auth/profile", params=update_data)
        assert response.status_code == 401