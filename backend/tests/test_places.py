import pytest
from app.models.place import Place

@pytest.mark.asyncio
async def test_get_places(client, db_session):
    """Test getting all places"""
    # Create test places
    places = [
        Place(
            name="Test City 1",
            latitude=12.9716,
            longitude=77.5946,
            timezone="Asia/Kolkata"
        ),
        Place(
            name="Test City 2",
            latitude=13.0827,
            longitude=80.2707,
            timezone="Asia/Kolkata"
        )
    ]
    for place in places:
        db_session.add(place)
    db_session.commit()
    
    # Make request to endpoint
    response = client.get("/api/places")
    
    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2  # Should have at least our test places
    assert any(p["name"] == "Test City 1" for p in data)
    assert any(p["name"] == "Test City 2" for p in data)

@pytest.mark.asyncio
async def test_get_place_by_id(client, db_session):
    """Test getting a place by ID"""
    # Create test place
    place = Place(
        name="Test City",
        latitude=12.9716,
        longitude=77.5946,
        timezone="Asia/Kolkata"
    )
    db_session.add(place)
    db_session.commit()
    
    # Make request to endpoint
    response = client.get(f"/api/places/{place.id}")
    
    # Assert response
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == place.id
    assert data["name"] == "Test City"
    assert data["latitude"] == 12.9716
    assert data["longitude"] == 77.5946
    assert data["timezone"] == "Asia/Kolkata"

@pytest.mark.asyncio
async def test_get_nonexistent_place(client):
    """Test getting a nonexistent place"""
    # Make request to endpoint with invalid ID
    response = client.get("/api/places/999999")
    
    # Assert response
    assert response.status_code == 404
    assert "Place not found" in response.json()["detail"] 