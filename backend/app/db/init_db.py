from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session
from app.models.base import Base
from app.models.place import Place
from app.models.horoscope import Horoscope
from app.models.translation import Translation
from app.models.matchmaking import Matchmaking
from app.db.session import engine, SessionLocal
from app.data.indian_districts import INDIAN_DISTRICTS
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_db(session: Session) -> None:
    """Initialize the database with required tables and data."""
    # Create all tables at once using metadata
    Base.metadata.create_all(bind=session.get_bind())
    logger.info("Created all database tables")
    
    # Check if places table is empty
    if session.query(Place).count() == 0:
        # Add Indian districts
        for district in INDIAN_DISTRICTS:
            place = Place(
                name=district['name'],
                latitude=district['latitude'],
                longitude=district['longitude'],
                timezone=district['timezone']
            )
            session.add(place)
        
        session.commit()
        logger.info("Database initialized with Indian districts data.")

if __name__ == "__main__":
    db = SessionLocal()
    try:
        init_db(db)
    finally:
        db.close() 