import pytest
from datetime import datetime
from app.models.place import Place
from app.models.horoscope import Horoscope

def test_create_place(db_session):
    """Test creating a place in the database"""
    place = Place(
        name="Erode",
        latitude=11.3428,
        longitude=77.7274,
        timezone="Asia/Kolkata"
    )
    db_session.add(place)
    db_session.commit()
    
    assert place.id is not None
    assert place.name == "Erode"
    assert place.latitude == 11.3428
    assert place.longitude == 77.7274
    assert place.timezone == "Asia/Kolkata"

def test_create_horoscope(db_session):
    """Test creating a horoscope in the database"""
    # First create a place
    place = Place(
        name="Erode",
        latitude=11.3428,
        longitude=77.7274,
        timezone="Asia/Kolkata"
    )
    db_session.add(place)
    db_session.commit()
    
    # Create horoscope
    horoscope = Horoscope(
        date_of_birth=datetime(1987, 3, 20).date(),
        time_of_birth=datetime.strptime("02:15", "%H:%M").time(),
        place_id=place.id,
        gender="male",
        rashi="Mesha",
        nakshatra="Ashwini",
        lagna="Mesha",
        planetary_positions={"sun": "Mesha", "moon": "Vrishabha"}
    )
    db_session.add(horoscope)
    db_session.commit()
    
    assert horoscope.id is not None
    assert horoscope.place_id == place.id
    assert horoscope.gender == "male"
    assert horoscope.rashi == "Mesha"
    assert horoscope.nakshatra == "Ashwini"
    assert horoscope.lagna == "Mesha"
    assert horoscope.planetary_positions == {"sun": "Mesha", "moon": "Vrishabha"}

@pytest.mark.asyncio
async def test_horoscope_calculation_endpoint(client, db_session):
    """Test the horoscope calculation endpoint"""
    # First create a place
    place = Place(
        name="Erode",
        latitude=11.3428,
        longitude=77.7274,
        timezone="Asia/Kolkata"
    )
    db_session.add(place)
    db_session.commit()
    
    # Test data
    test_data = {
        "date_of_birth": "1987-03-20",
        "time_of_birth": "02:15",
        "place_id": place.id,
        "gender": "male"
    }
    
    # Make request to endpoint
    response = client.post("/api/horoscope/calculate", json=test_data)
    
    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert "id" in data
    assert "rashi" in data
    assert "nakshatra" in data
    assert "lagna" in data
    assert "planetary_positions" in data
    assert data["place_id"] == place.id
    assert data["gender"] == "male"

@pytest.mark.asyncio
async def test_get_horoscope_endpoint(client, db_session):
    """Test getting a horoscope by ID"""
    # First create a place and horoscope
    place = Place(
        name="Erode",
        latitude=11.3428,
        longitude=77.7274,
        timezone="Asia/Kolkata"
    )
    db_session.add(place)
    db_session.commit()
    
    horoscope = Horoscope(
        date_of_birth=datetime(1987, 3, 20).date(),
        time_of_birth=datetime.strptime("02:15", "%H:%M").time(),
        place_id=place.id,
        gender="male",
        rashi="Mesha",
        nakshatra="Ashwini",
        lagna="Mesha",
        planetary_positions={"sun": "Mesha", "moon": "Vrishabha"}
    )
    db_session.add(horoscope)
    db_session.commit()
    
    # Make request to endpoint
    response = client.get(f"/api/horoscope/{horoscope.id}")
    
    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == horoscope.id
    assert data["place_id"] == place.id
    assert data["gender"] == "male"
    assert data["rashi"] == "Mesha"
    assert data["nakshatra"] == "Ashwini"
    assert data["lagna"] == "Mesha"
    assert data["planetary_positions"] == {"sun": "Mesha", "moon": "Vrishabha"}

@pytest.mark.asyncio
async def test_invalid_horoscope_request(client):
    """Test invalid horoscope calculation request"""
    # Test data with invalid date format
    test_data = {
        "date_of_birth": "invalid-date",
        "time_of_birth": "02:15",
        "place_id": 1,
        "gender": "male"
    }
    
    # Make request to endpoint
    response = client.post("/api/horoscope/calculate", json=test_data)
    
    # Assert response
    assert response.status_code == 400
    assert "Invalid date/time format" in response.json()["detail"] 