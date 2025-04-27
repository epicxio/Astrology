import pytest
import os
from app.services.pdf_generator import PDFGenerator

@pytest.fixture
def pdf_generator():
    return PDFGenerator()

@pytest.fixture
def sample_horoscope_data():
    return {
        "name": "Vinay",
        "date_of_birth": "1987-03-20",
        "time_of_birth": "02:15",
        "place_of_birth": "Erode",
        "rashi": "Mesha",
        "nakshatra": "Ashwini",
        "lagna": "Mesha",
        "planetary_positions": {
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
    }

@pytest.fixture
def sample_matchmaking_data():
    return {
        "bride": {
            "name": "Jane Doe",
            "date_of_birth": "1992-05-15",
            "time_of_birth": "14:30",
            "place_of_birth": "Chennai",
            "rashi": "Kataka",
            "nakshatra": "Pushya"
        },
        "groom": {
            "name": "Vinay",
            "date_of_birth": "1987-03-20",
            "time_of_birth": "02:15",
            "place_of_birth": "Erode",
            "rashi": "Mesha",
            "nakshatra": "Ashwini"
        },
        "match_score": 28,
        "compatibility": "Excellent",
        "remarks": "Very good match with strong compatibility in all aspects."
    }

def test_generate_horoscope_pdf(pdf_generator, sample_horoscope_data):
    """Test generating a horoscope PDF report"""
    # Generate PDF
    filename = pdf_generator.generate_horoscope_pdf(sample_horoscope_data)
    
    # Check if file was created
    assert os.path.exists(filename)
    assert filename.endswith(".pdf")
    
    # Clean up
    os.remove(filename)

def test_generate_matchmaking_pdf(pdf_generator, sample_matchmaking_data):
    """Test generating a matchmaking PDF report"""
    # Generate PDF
    filename = pdf_generator.generate_matchmaking_pdf(sample_matchmaking_data)
    
    # Check if file was created
    assert os.path.exists(filename)
    assert filename.endswith(".pdf")
    
    # Clean up
    os.remove(filename)

def test_generate_horoscope_pdf_with_language(pdf_generator, sample_horoscope_data):
    """Test generating a horoscope PDF report with different languages"""
    # Test with English
    filename_en = pdf_generator.generate_horoscope_pdf(sample_horoscope_data, language="en")
    assert os.path.exists(filename_en)
    os.remove(filename_en)
    
    # Test with Malayalam
    filename_ml = pdf_generator.generate_horoscope_pdf(sample_horoscope_data, language="ml")
    assert os.path.exists(filename_ml)
    os.remove(filename_ml)
    
    # Test with Tamil
    filename_ta = pdf_generator.generate_horoscope_pdf(sample_horoscope_data, language="ta")
    assert os.path.exists(filename_ta)
    os.remove(filename_ta)

def test_generate_matchmaking_pdf_with_language(pdf_generator, sample_matchmaking_data):
    """Test generating a matchmaking PDF report with different languages"""
    # Test with English
    filename_en = pdf_generator.generate_matchmaking_pdf(sample_matchmaking_data, language="en")
    assert os.path.exists(filename_en)
    os.remove(filename_en)
    
    # Test with Malayalam
    filename_ml = pdf_generator.generate_matchmaking_pdf(sample_matchmaking_data, language="ml")
    assert os.path.exists(filename_ml)
    os.remove(filename_ml)
    
    # Test with Tamil
    filename_ta = pdf_generator.generate_matchmaking_pdf(sample_matchmaking_data, language="ta")
    assert os.path.exists(filename_ta)
    os.remove(filename_ta) 