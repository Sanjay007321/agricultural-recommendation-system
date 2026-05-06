import pytest
from fastapi.testclient import TestClient
from datetime import datetime

class TestAnalysisAPI:
    """Test analysis endpoints"""
    
    def test_analyze_crop_success(self, client: TestClient, auth_headers):
        """Test successful crop analysis"""
        analysis_data = {
            "season": "Kharif",
            "soil_type": "Clay",
            "soil_ph": 6.5,
            "previous_crop": "Wheat",
            "nitrogen_level": 45,
            "phosphorus_level": 35,
            "potassium_level": 30,
            "land_size_acres": 5.0,
            "water_source": "Well",
            "rainfall_mm": 800,
            "temperature_celsius": 28,
            "market_distance_km": 25,
            "storage_available": True,
            "crop_preference": "auto",
            "investment_limit": 50000
        }
        
        response = client.post("/api/analyze", json=analysis_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert "analysis_id" in data
        assert "crop_recommendation" in data
        assert "yield_prediction" in data
        assert "price_prediction" in data
        assert "profit_analysis" in data
        assert data["analysis_id"].startswith("ANL-")
    
    def test_analyze_crop_specific_crop(self, client: TestClient, auth_headers):
        """Test analysis with specific crop preference"""
        analysis_data = {
            "season": "Rabi",
            "soil_type": "Loamy",
            "soil_ph": 7.0,
            "previous_crop": "Rice",
            "nitrogen_level": 40,
            "phosphorus_level": 30,
            "potassium_level": 25,
            "land_size_acres": 3.0,
            "water_source": "Canal",
            "rainfall_mm": 400,
            "temperature_celsius": 22,
            "market_distance_km": 15,
            "storage_available": False,
            "crop_preference": "Wheat",  # Specific crop
            "investment_limit": 30000
        }
        
        response = client.post("/api/analyze", json=analysis_data, headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["crop_recommendation"]["recommended_crop"] == "Wheat"
    
    def test_analyze_crop_missing_fields(self, client: TestClient, auth_headers):
        """Test analysis with missing required fields"""
        incomplete_data = {
            "season": "Kharif",
            "soil_type": "Clay"
            # Missing many required fields
        }
        
        response = client.post("/api/analyze", json=incomplete_data, headers=auth_headers)
        assert response.status_code == 422  # Validation error
    
    def test_analyze_crop_unauthenticated(self, client: TestClient):
        """Test analysis without authentication"""
        analysis_data = {
            "season": "Kharif",
            "soil_type": "Clay",
            "soil_ph": 6.5,
            "land_size_acres": 5.0
        }
        
        response = client.post("/api/analyze", json=analysis_data)
        assert response.status_code == 401
    
    def test_get_analysis_history(self, client: TestClient, auth_headers):
        """Test getting analysis history"""
        # First create an analysis
        analysis_data = {
            "season": "Kharif",
            "soil_type": "Clay",
            "soil_ph": 6.5,
            "previous_crop": "Wheat",
            "nitrogen_level": 45,
            "phosphorus_level": 35,
            "potassium_level": 30,
            "land_size_acres": 5.0,
            "water_source": "Well",
            "rainfall_mm": 800,
            "temperature_celsius": 28,
            "market_distance_km": 25,
            "storage_available": True,
            "crop_preference": "auto",
            "investment_limit": 50000
        }
        
        # Create analysis
        client.post("/api/analyze", json=analysis_data, headers=auth_headers)
        
        # Get history
        response = client.get("/api/history", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        if len(data) > 0:
            assert "analysis_id" in data[0]
            assert "crop" in data[0]
            assert "profit" in data[0]
    
    def test_get_analysis_history_empty(self, client: TestClient, auth_headers):
        """Test getting history when no analyses exist"""
        response = client.get("/api/history", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        # May be empty or contain some default data
    
    def test_get_analysis_history_unauthenticated(self, client: TestClient):
        """Test getting history without authentication"""
        response = client.get("/api/history")
        assert response.status_code == 401
    
    def test_get_analysis_detail_success(self, client: TestClient, auth_headers):
        """Test getting specific analysis details"""
        # First create an analysis
        analysis_data = {
            "season": "Rabi",
            "soil_type": "Loamy",
            "soil_ph": 7.0,
            "previous_crop": "Rice",
            "nitrogen_level": 40,
            "phosphorus_level": 30,
            "potassium_level": 25,
            "land_size_acres": 3.0,
            "water_source": "Canal",
            "rainfall_mm": 400,
            "temperature_celsius": 22,
            "market_distance_km": 15,
            "storage_available": False,
            "crop_preference": "Wheat",
            "investment_limit": 30000
        }
        
        # Create analysis and get analysis_id
        create_response = client.post("/api/analyze", json=analysis_data, headers=auth_headers)
        assert create_response.status_code == 200
        analysis_id = create_response.json()["analysis_id"]
        
        # Get analysis details
        response = client.get(f"/api/history/{analysis_id}", headers=auth_headers)
        assert response.status_code == 200
        
        data = response.json()
        assert data["analysis_id"] == analysis_id
        assert "crop_recommendation" in data
        assert "yield_prediction" in data
    
    def test_get_analysis_detail_not_found(self, client: TestClient, auth_headers):
        """Test getting non-existent analysis"""
        fake_analysis_id = "ANL-20240101-00000"
        response = client.get(f"/api/history/{fake_analysis_id}", headers=auth_headers)
        assert response.status_code == 404
    
    def test_get_analysis_detail_wrong_user(self, client: TestClient, auth_headers, test_user):
        """Test accessing another user's analysis (should fail)"""
        # This test assumes analyses are user-specific
        # Implementation depends on how the backend handles user isolation
        pass  # Placeholder - implement based on actual security model
    
    def test_get_crops_list(self, client: TestClient):
        """Test getting list of supported crops"""
        response = client.get("/api/crops")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        # Check that crop data has expected structure
        sample_crop = data[0]
        assert "name" in sample_crop
        assert "seasons" in sample_crop
        assert "soil_types" in sample_crop
    
    def test_get_schemes_list(self, client: TestClient):
        """Test getting list of government schemes"""
        response = client.get("/api/schemes")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        # Check structure of scheme data
        if len(data) > 0:
            sample_scheme = data[0]
            assert "scheme_name" in sample_scheme
            assert "description" in sample_scheme
            assert "eligibility_criteria" in sample_scheme
    
    def test_get_states_list(self, client: TestClient):
        """Test getting list of states with districts"""
        response = client.get("/api/states")
        assert response.status_code == 200
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0
        
        sample_state = data[0]
        assert "name" in sample_state
        assert "code" in sample_state
        assert "districts" in sample_state
        assert isinstance(sample_state["districts"], list)