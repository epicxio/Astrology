import pytest
from app.models.translation import Translation
from app.services.translations import get_translation

@pytest.fixture
def sample_translations(db_session):
    """Create sample translations in the database"""
    translations = [
        Translation(
            key="welcome",
            language="en",
            value="Welcome to Epic-X Horoscope"
        ),
        Translation(
            key="welcome",
            language="ml",
            value="എപിക്-എക്സ് ജ്യോതിഷത്തിലേക്ക് സ്വാഗതം"
        ),
        Translation(
            key="welcome",
            language="ta",
            value="எபிக்-எக்ஸ் ஜோதிடத்திற்கு வரவேற்கிறோம்"
        ),
        Translation(
            key="calculate_horoscope",
            language="en",
            value="Calculate Horoscope"
        ),
        Translation(
            key="calculate_horoscope",
            language="ml",
            value="ജ്യോതിഷം കണക്കാക്കുക"
        ),
        Translation(
            key="calculate_horoscope",
            language="ta",
            value="ஜோதிடத்தை கணக்கிடு"
        )
    ]
    
    for translation in translations:
        db_session.add(translation)
    db_session.commit()
    
    return translations

@pytest.mark.asyncio
async def test_get_translation(db_session, sample_translations):
    """Test getting translations for different languages"""
    # Test English translation
    en_translation = get_translation("welcome", "en", db_session)
    assert en_translation == "Welcome to Epic-X Horoscope"
    
    # Test Malayalam translation
    ml_translation = get_translation("welcome", "ml", db_session)
    assert ml_translation == "എപിക്-എക്സ് ജ്യോതിഷത്തിലേക്ക് സ്വാഗതം"
    
    # Test Tamil translation
    ta_translation = get_translation("welcome", "ta", db_session)
    assert ta_translation == "எபிக்-எக்ஸ் ஜோதிடத்திற்கு வரவேற்கிறோம்"

@pytest.mark.asyncio
async def test_get_nonexistent_translation(db_session):
    """Test getting nonexistent translation"""
    # Test with nonexistent key
    translation = get_translation("nonexistent_key", "en", db_session)
    assert translation is None
    
    # Test with nonexistent language
    translation = get_translation("welcome", "fr", db_session)
    assert translation is None

@pytest.mark.asyncio
async def test_get_translation_with_fallback(db_session, sample_translations):
    """Test getting translation with fallback to English"""
    # Test with nonexistent language (should fallback to English)
    translation = get_translation("welcome", "fr", db_session, fallback=True)
    assert translation == "Welcome to Epic-X Horoscope"
    
    # Test with nonexistent key (should return None even with fallback)
    translation = get_translation("nonexistent_key", "fr", db_session, fallback=True)
    assert translation is None 