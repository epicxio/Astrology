import pytest
from datetime import datetime, date, time
from app.services.horoscope_calculator import calculate_horoscope

@pytest.mark.asyncio
async def test_calculate_horoscope():
    """Test horoscope calculation with valid input"""
    # Test data
    date_of_birth = date(1987, 3, 20)
    time_of_birth = time(2, 15)
    latitude = 11.3428  # Erode coordinates
    longitude = 77.7274
    timezone = "Asia/Kolkata"
    gender = "male"
    
    # Calculate horoscope
    result = calculate_horoscope(
        date_of_birth=date_of_birth,
        time_of_birth=time_of_birth,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        gender=gender
    )
    
    # Assert result structure
    assert isinstance(result, dict)
    assert "rashi" in result
    assert "nakshatra" in result
    assert "lagna" in result
    assert "planetary_positions" in result
    
    # Assert planetary positions
    assert isinstance(result["planetary_positions"], dict)
    assert "sun" in result["planetary_positions"]
    assert "moon" in result["planetary_positions"]
    assert "mars" in result["planetary_positions"]
    assert "mercury" in result["planetary_positions"]
    assert "jupiter" in result["planetary_positions"]
    assert "venus" in result["planetary_positions"]
    assert "saturn" in result["planetary_positions"]
    assert "rahu" in result["planetary_positions"]
    assert "ketu" in result["planetary_positions"]

@pytest.mark.asyncio
async def test_calculate_horoscope_with_different_gender():
    """Test horoscope calculation with different gender"""
    # Test data
    date_of_birth = date(1987, 3, 20)
    time_of_birth = time(2, 15)
    latitude = 11.3428  # Erode coordinates
    longitude = 77.7274
    timezone = "Asia/Kolkata"
    
    # Calculate for male
    result_male = calculate_horoscope(
        date_of_birth=date_of_birth,
        time_of_birth=time_of_birth,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        gender="male"
    )
    
    # Calculate for female
    result_female = calculate_horoscope(
        date_of_birth=date_of_birth,
        time_of_birth=time_of_birth,
        latitude=latitude,
        longitude=longitude,
        timezone=timezone,
        gender="female"
    )
    
    # Assert both results have same structure
    assert result_male.keys() == result_female.keys()
    assert result_male["planetary_positions"].keys() == result_female["planetary_positions"].keys()

@pytest.mark.asyncio
async def test_calculate_horoscope_with_different_location():
    """Test horoscope calculation with different locations"""
    # Test data for Erode
    date_of_birth = date(1987, 3, 20)
    time_of_birth = time(2, 15)
    timezone = "Asia/Kolkata"
    
    # Calculate for Erode
    result_erode = calculate_horoscope(
        date_of_birth=date_of_birth,
        time_of_birth=time_of_birth,
        latitude=11.3428,
        longitude=77.7274,
        timezone=timezone,
        gender="male"
    )
    
    # Calculate for Chennai
    result_chennai = calculate_horoscope(
        date_of_birth=date_of_birth,
        time_of_birth=time_of_birth,
        latitude=13.0827,
        longitude=80.2707,
        timezone=timezone,
        gender="male"
    )
    
    # Assert both results have same structure
    assert result_erode.keys() == result_chennai.keys()
    assert result_erode["planetary_positions"].keys() == result_chennai["planetary_positions"].keys()
    
    # The actual values might be different due to different locations
    assert result_erode != result_chennai 