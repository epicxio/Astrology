import pytest
from datetime import datetime, date, time
from app.models.horoscope import Horoscope
from app.models.place import Place
from app.services.pdf_generator import PDFGenerator

@pytest.fixture
def sample_horoscope_data(db_session):
    """Create sample horoscope data in the database"""
    # Create place
    place = Place(
        name="Test City",
        latitude=12.9716,
        longitude=77.5946,
        timezone="Asia/Kolkata"
    )
    db_session.add(place)
    db_session.commit()
    
    # Create horoscope
    horoscope = Horoscope(
        date_of_birth=date(1990, 1, 1),
        time_of_birth=time(12, 0),
        place_id=place.id,
        gender="male",
        rashi="Mesha",
        nakshatra="Ashwini",
        lagna="Mesha",
        planetary_positions={
            "sun": "Mesha",
            "moon": "Vrishabha",
            "mars": "Mithuna",
            "mercury": "Kataka",
            "jupiter": "Simha",
            "venus": "Kanya",
            "saturn": "Thula",
            "rahu": "Dhanu",
            "ketu": "Mithuna"
        }
    )
    db_session.add(horoscope)
    db_session.commit()
    
    return horoscope

@pytest.mark.asyncio
async def test_generate_horoscope_report(client, sample_horoscope_data):
    """Test generating a horoscope PDF report"""
    # Make request to endpoint
    response = client.get(f"/api/reports/horoscope/{sample_horoscope_data.id}")
    
    # Assert response
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert f"horoscope_{sample_horoscope_data.id}.pdf" in response.headers["content-disposition"]

@pytest.mark.asyncio
async def test_generate_horoscope_report_with_language(client, sample_horoscope_data):
    """Test generating a horoscope PDF report with different languages"""
    # Test with English
    response_en = client.get(f"/api/reports/horoscope/{sample_horoscope_data.id}?language=en")
    assert response_en.status_code == 200
    assert response_en.headers["content-type"] == "application/pdf"
    
    # Test with Malayalam
    response_ml = client.get(f"/api/reports/horoscope/{sample_horoscope_data.id}?language=ml")
    assert response_ml.status_code == 200
    assert response_ml.headers["content-type"] == "application/pdf"
    
    # Test with Tamil
    response_ta = client.get(f"/api/reports/horoscope/{sample_horoscope_data.id}?language=ta")
    assert response_ta.status_code == 200
    assert response_ta.headers["content-type"] == "application/pdf"

@pytest.mark.asyncio
async def test_generate_nonexistent_horoscope_report(client):
    """Test generating a report for nonexistent horoscope"""
    # Make request to endpoint with invalid ID
    response = client.get("/api/reports/horoscope/999999")
    
    # Assert response
    assert response.status_code == 404
    assert "Horoscope not found" in response.json()["detail"]

@pytest.mark.asyncio
async def test_generate_matchmaking_report(client, sample_horoscope_data):
    """Test generating a matchmaking PDF report"""
    # Create another horoscope for matchmaking
    place = db_session.query(Place).first()
    horoscope2 = Horoscope(
        date_of_birth=date(1992, 5, 15),
        time_of_birth=time(14, 30),
        place_id=place.id,
        gender="female",
        rashi="Kataka",
        nakshatra="Pushya",
        lagna="Kataka",
        planetary_positions={
            "sun": "Kataka",
            "moon": "Simha",
            "mars": "Thula",
            "mercury": "Vrishchika",
            "jupiter": "Dhanu",
            "venus": "Makara",
            "saturn": "Kumbha",
            "rahu": "Meena",
            "ketu": "Kanya"
        }
    )
    db_session.add(horoscope2)
    db_session.commit()
    
    # Make request to endpoint
    response = client.get(f"/api/reports/matchmaking/{sample_horoscope_data.id}/{horoscope2.id}")
    
    # Assert response
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/pdf"
    assert "attachment" in response.headers["content-disposition"]
    assert f"matchmaking_{sample_horoscope_data.id}_{horoscope2.id}.pdf" in response.headers["content-disposition"]

@pytest.mark.asyncio
async def test_generate_matchmaking_report_with_language(client, sample_horoscope_data):
    """Test generating a matchmaking PDF report with different languages"""
    # Create another horoscope for matchmaking
    place = db_session.query(Place).first()
    horoscope2 = Horoscope(
        date_of_birth=date(1992, 5, 15),
        time_of_birth=time(14, 30),
        place_id=place.id,
        gender="female",
        rashi="Kataka",
        nakshatra="Pushya",
        lagna="Kataka",
        planetary_positions={
            "sun": "Kataka",
            "moon": "Simha",
            "mars": "Thula",
            "mercury": "Vrishchika",
            "jupiter": "Dhanu",
            "venus": "Makara",
            "saturn": "Kumbha",
            "rahu": "Meena",
            "ketu": "Kanya"
        }
    )
    db_session.add(horoscope2)
    db_session.commit()
    
    # Test with English
    response_en = client.get(f"/api/reports/matchmaking/{sample_horoscope_data.id}/{horoscope2.id}?language=en")
    assert response_en.status_code == 200
    assert response_en.headers["content-type"] == "application/pdf"
    
    # Test with Malayalam
    response_ml = client.get(f"/api/reports/matchmaking/{sample_horoscope_data.id}/{horoscope2.id}?language=ml")
    assert response_ml.status_code == 200
    assert response_ml.headers["content-type"] == "application/pdf"
    
    # Test with Tamil
    response_ta = client.get(f"/api/reports/matchmaking/{sample_horoscope_data.id}/{horoscope2.id}?language=ta")
    assert response_ta.status_code == 200
    assert response_ta.headers["content-type"] == "application/pdf" 