import pytest
from fastapi.testclient import TestClient
import base64
import io
from PIL import Image

class TestFunctionalFlow:
    """Comprehensive functional tests for the Crop Management System"""

    def test_system_health(self, client: TestClient):
        """Verify the API is up and running"""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "healthy"

        response = client.get("/")
        assert response.status_code == 200
        assert "version" in response.json()

    def test_authentication_flow(self, client: TestClient):
        """Test full user registration and login flow"""
        # 1. Register a new user
        user_data = {
            "full_name": "Functional Test Farmer",
            "mobile": "9876543210",
            "password": "testpassword123",
            "state": "Maharashtra",
            "district": "Pune",
            "village": "Test Village",
            "land_size_acres": 5.0
        }
        
        # Check if user already exists, if so, we'll just login
        reg_response = client.post("/api/auth/register", json=user_data)
        if reg_response.status_code == 200:
            data = reg_response.json()
            assert "access_token" in data
            assert "farmer_id" in data
        else:
            # If registration fails (e.g. duplicate mobile), we'll try login
            pass

        # 2. Login
        login_data = {
            "mobile": user_data["mobile"],
            "password": user_data["password"]
        }
        login_response = client.post("/api/auth/login", json=login_data)
        assert login_response.status_code == 200
        token_data = login_response.json()
        access_token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}

        # 3. Get current user info
        me_response = client.get("/api/auth/me", headers=headers)
        assert me_response.status_code == 200
        user_info = me_response.json()
        assert user_info["full_name"] == user_data["full_name"]
        assert user_info["mobile"] == user_data["mobile"]

    def test_reference_data(self, client: TestClient):
        """Verify reference data endpoints are working"""
        # States and Districts
        response = client.get("/api/states")
        assert response.status_code == 200
        states = response.json()
        assert len(states) > 0
        assert "name" in states[0]
        assert "districts" in states[0]

        # Crops list
        response = client.get("/api/crops")
        assert response.status_code == 200
        crops = response.json()
        assert len(crops) > 0

        # Schemes list
        response = client.get("/api/schemes")
        assert response.status_code == 200
        schemes = response.json()
        assert len(schemes) > 0

    def test_analysis_flow(self, client: TestClient, auth_headers):
        """Test the core crop analysis and history flow"""
        # 1. Run analysis
        analysis_input = {
            "land_area_acres": 2.5,
            "soil_type": "Black Soil",
            "soil_ph": 7.2,
            "nitrogen": 150.0,
            "phosphorus": 60.0,
            "potassium": 45.0,
            "state": "Maharashtra",
            "district": "Pune",
            "season": "Kharif",
            "rainfall_mm": 1200.0,
            "temperature_c": 30.5,
            "humidity_percent": 75.0,
            "budget_inr": 50000.0,
            "crop_preference": "auto",
            "nearest_mandi": "Pune Mandi",
            "sowing_date": "2024-06-15"
        }
        
        response = client.post("/api/analyze", json=analysis_input, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        assert "analysis_id" in data
        assert "crop_recommendation" in data
        assert "profit_analysis" in data
        analysis_id = data["analysis_id"]

        # 2. Check History
        history_response = client.get("/api/history", headers=auth_headers)
        assert history_response.status_code == 200
        history = history_response.json()
        assert any(h["analysis_id"] == analysis_id for h in history)

        # 3. Get Detail
        detail_response = client.get(f"/api/history/{analysis_id}", headers=auth_headers)
        assert detail_response.status_code == 200
        assert detail_response.json()["analysis_id"] == analysis_id

    def test_soil_image_analysis(self, client: TestClient, auth_headers):
        """Test soil analysis using a dummy base64 image"""
        # Create a small dummy image
        img = Image.new('RGB', (100, 100), color=(120, 80, 50)) # Brownish color for soil
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        
        image_data = {
            "image_base64": f"data:image/jpeg;base64,{img_str}"
        }
        
        response = client.post("/api/soil/analyze-base64", json=image_data, headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        assert data["success"] is True
        assert "data" in data
        assert "soil_type" in data["data"]
        assert "soil_ph" in data["data"]

    def test_climate_dashboard(self, client: TestClient, auth_headers):
        """Test the climate dashboard endpoint"""
        response = client.get("/api/climate-dashboard", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        
        assert "current_weather" in data
        assert "weather_forecast" in data
        assert "soil_data" in data
        assert "weather_analysis" in data
