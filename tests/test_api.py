"""
Unit tests for FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from api.app import app

client = TestClient(app)

class TestAPIEndpoints:
    """Test API endpoints"""
    
    def test_root_endpoint(self):
        """Test root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["status"] == "active"
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert "status" in data
        assert "timestamp" in data
    
    def test_predict_endpoint_valid_input(self):
        """Test prediction with valid input"""
        payload = {
            "age": 63,
            "sex": 1,
            "cp": 3,
            "trestbps": 145,
            "chol": 233,
            "fbs": 1,
            "restecg": 0,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 2.3,
            "slope": 0,
            "ca": 0,
            "thal": 1
        }
        
        response = client.post("/predict", json=payload)
        
        # If model is loaded
        if response.status_code == 200:
            data = response.json()
            assert "prediction" in data
            assert "probability" in data
            assert "risk_level" in data
            assert data["prediction"] in [0, 1]
            assert 0 <= data["probability"] <= 1
        # If model not loaded (503 Service Unavailable)
        else:
            assert response.status_code == 503
    
    def test_predict_endpoint_invalid_input(self):
        """Test prediction with invalid input"""
        # Missing required field
        payload = {
            "age": 63,
            "sex": 1,
            # Missing other required fields
        }
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_predict_endpoint_out_of_range(self):
        """Test prediction with out of range values"""
        payload = {
            "age": 200,  # Invalid age
            "sex": 1,
            "cp": 3,
            "trestbps": 145,
            "chol": 233,
            "fbs": 1,
            "restecg": 0,
            "thalach": 150,
            "exang": 0,
            "oldpeak": 2.3,
            "slope": 0,
            "ca": 0,
            "thal": 1
        }
        
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
    
    def test_metrics_endpoint(self):
        """Test metrics endpoint"""
        response = client.get("/metrics")
        assert response.status_code == 200
        data = response.json()
        assert "total_predictions" in data

class TestAPIValidation:
    """Test input validation"""
    
    def test_age_validation(self):
        """Test age field validation"""
        base_payload = {
            "sex": 1, "cp": 3, "trestbps": 145, "chol": 233,
            "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0,
            "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
        }
        
        # Valid age
        payload = {**base_payload, "age": 50}
        response = client.post("/predict", json=payload)
        assert response.status_code in [200, 503]
        
        # Invalid age (negative)
        payload = {**base_payload, "age": -1}
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
        
        # Invalid age (too high)
        payload = {**base_payload, "age": 150}
        response = client.post("/predict", json=payload)
        assert response.status_code == 422
    
    def test_sex_validation(self):
        """Test sex field validation"""
        base_payload = {
            "age": 50, "cp": 3, "trestbps": 145, "chol": 233,
            "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0,
            "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
        }
        
        # Valid sex values
        for sex in [0, 1]:
            payload = {**base_payload, "sex": sex}
            response = client.post("/predict", json=payload)
            assert response.status_code in [200, 503]
        
        # Invalid sex
        payload = {**base_payload, "sex": 2}
        response = client.post("/predict", json=payload)
        assert response.status_code == 422

class TestAPIResponse:
    """Test API response structure"""
    
    def test_response_structure(self):
        """Test that response has correct structure"""
        payload = {
            "age": 63, "sex": 1, "cp": 3, "trestbps": 145,
            "chol": 233, "fbs": 1, "restecg": 0, "thalach": 150,
            "exang": 0, "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
        }
        
        response = client.post("/predict", json=payload)
        
        if response.status_code == 200:
            data = response.json()
            
            # Check required fields
            required_fields = ["prediction", "probability", "risk_level", "message", "timestamp"]
            for field in required_fields:
                assert field in data
            
            # Check data types
            assert isinstance(data["prediction"], int)
            assert isinstance(data["probability"], float)
            assert isinstance(data["risk_level"], str)
            assert isinstance(data["message"], str)
            assert isinstance(data["timestamp"], str)
            
            # Check value ranges
            assert data["prediction"] in [0, 1]
            assert 0 <= data["probability"] <= 1
            assert data["risk_level"] in ["Low", "Medium", "High"]

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
