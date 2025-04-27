import pytest
from datetime import datetime, date, time
from app.services.matchmaking import calculate_matchmaking

@pytest.fixture
def sample_bride_data():
    return {
        "date_of_birth": date(1992, 5, 15),
        "time_of_birth": time(14, 30),
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone": "Asia/Kolkata",
        "gender": "female"
    }

@pytest.fixture
def sample_groom_data():
    return {
        "date_of_birth": date(1990, 1, 1),
        "time_of_birth": time(12, 0),
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone": "Asia/Kolkata",
        "gender": "male"
    }

@pytest.mark.asyncio
async def test_calculate_matchmaking(sample_bride_data, sample_groom_data):
    """Test matchmaking calculation with valid input"""
    # Calculate matchmaking
    result = calculate_matchmaking(sample_bride_data, sample_groom_data)
    
    # Assert result structure
    assert isinstance(result, dict)
    assert "match_score" in result
    assert "compatibility" in result
    assert "remarks" in result
    assert "guna_milan" in result
    
    # Assert match score is within valid range
    assert 0 <= result["match_score"] <= 36
    
    # Assert guna milan details
    assert isinstance(result["guna_milan"], dict)
    assert "varna" in result["guna_milan"]
    assert "vashya" in result["guna_milan"]
    assert "tara" in result["guna_milan"]
    assert "yoni" in result["guna_milan"]
    assert "graha_maitri" in result["guna_milan"]
    assert "gana" in result["guna_milan"]
    assert "bhakoot" in result["guna_milan"]
    assert "nadi" in result["guna_milan"]

@pytest.mark.asyncio
async def test_calculate_matchmaking_with_same_birth_details(sample_bride_data):
    """Test matchmaking calculation with same birth details"""
    # Use same data for both bride and groom
    result = calculate_matchmaking(sample_bride_data, sample_bride_data)
    
    # Assert result structure
    assert isinstance(result, dict)
    assert "match_score" in result
    assert "compatibility" in result
    assert "remarks" in result
    
    # Assert match score is within valid range
    assert 0 <= result["match_score"] <= 36

@pytest.mark.asyncio
async def test_calculate_matchmaking_with_different_locations():
    """Test matchmaking calculation with different locations"""
    # Bride data (Bangalore)
    bride_data = {
        "date_of_birth": date(1992, 5, 15),
        "time_of_birth": time(14, 30),
        "latitude": 12.9716,
        "longitude": 77.5946,
        "timezone": "Asia/Kolkata",
        "gender": "female"
    }
    
    # Groom data (Delhi)
    groom_data = {
        "date_of_birth": date(1990, 1, 1),
        "time_of_birth": time(12, 0),
        "latitude": 28.7041,
        "longitude": 77.1025,
        "timezone": "Asia/Kolkata",
        "gender": "male"
    }
    
    # Calculate matchmaking
    result = calculate_matchmaking(bride_data, groom_data)
    
    # Assert result structure
    assert isinstance(result, dict)
    assert "match_score" in result
    assert "compatibility" in result
    assert "remarks" in result
    
    # Assert match score is within valid range
    assert 0 <= result["match_score"] <= 36 