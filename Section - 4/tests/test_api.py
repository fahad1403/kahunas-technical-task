import pytest
from fastapi.testclient import TestClient
import sys
import os
from datetime import datetime

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_server import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert data["status"] == "healthy"
    assert "timestamp" in data

def test_get_fitness_data():
    user_id = "test_user"
    response = client.get(f"/api/v1/fitness/data/{user_id}")
    assert response.status_code == 200
    data = response.json()
    
    # Check data structure
    assert "user_id" in data
    assert "timestamp" in data
    assert "steps" in data
    assert "heart_rate" in data
    
    # Validate data types and ranges
    assert data["user_id"] == user_id
    assert isinstance(data["steps"], int)
    assert 0 <= data["steps"] <= 500
    assert isinstance(data["heart_rate"], int)
    assert 60 <= data["heart_rate"] <= 150

def test_get_fitness_data_invalid_user():
    response = client.get("/api/v1/fitness/data/ ")
    assert response.status_code == 400
    assert "Invalid user ID" in response.json()["detail"]

def test_get_user_stats():
    # First, generate some fitness data
    user_id = "test_user"
    client.get(f"/api/v1/fitness/data/{user_id}")
    
    # Then get stats
    response = client.get(f"/api/v1/fitness/stats/{user_id}")
    assert response.status_code == 200
    data = response.json()
    
    # Check data structure
    assert "user_id" in data
    assert "total_steps" in data
    assert "average_heart_rate" in data
    assert "active_minutes" in data
    
    # Validate data types and ranges
    assert data["user_id"] == user_id
    assert isinstance(data["total_steps"], int)
    assert isinstance(data["average_heart_rate"], int)
    assert isinstance(data["active_minutes"], int)
    assert 5000 <= data["total_steps"] <= 15000
    assert 70 <= data["average_heart_rate"] <= 90
    assert 30 <= data["active_minutes"] <= 180

def test_get_user_stats_nonexistent_user():
    response = client.get("/api/v1/fitness/stats/nonexistent_user")
    assert response.status_code == 404
    assert "User not found" in response.json()["detail"] 