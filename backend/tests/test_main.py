import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Epic-X Horoscope API" in response.json()["message"]

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_api_docs():
    """Test the API documentation endpoints"""
    # Test Swagger UI
    response = client.get("/docs")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    
    # Test OpenAPI schema
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"
    assert "openapi" in response.json()
    assert "info" in response.json()
    assert "paths" in response.json()

def test_cors_headers():
    """Test CORS headers"""
    response = client.get("/")
    assert "access-control-allow-origin" in response.headers
    assert "access-control-allow-methods" in response.headers
    assert "access-control-allow-headers" in response.headers

def test_error_handling():
    """Test error handling"""
    # Test 404 error
    response = client.get("/nonexistent-endpoint")
    assert response.status_code == 404
    assert "detail" in response.json()
    
    # Test 500 error (simulated)
    response = client.get("/simulate-error")
    assert response.status_code == 500
    assert "detail" in response.json()

def test_rate_limiting():
    """Test rate limiting"""
    # Make multiple requests in quick succession
    for _ in range(5):
        response = client.get("/")
        assert response.status_code == 200
    
    # The next request should be rate limited
    response = client.get("/")
    assert response.status_code == 429
    assert "Too Many Requests" in response.json()["detail"] 