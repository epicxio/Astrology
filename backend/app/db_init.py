from sqlalchemy import create_engine
from app.config.database import Base
from app.models.place import Place
from app.models.horoscope import Horoscope
from app.models.matchmaking import Matchmaking
from app.models.translation import Translation
from app.config.settings import settings

def init_db():
    # Create engine
    engine = create_engine(settings.DATABASE_URL)
    
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a session
    from sqlalchemy.orm import sessionmaker
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Add some initial places
        places = [
            Place(name="Kochi", state="Kerala", country="India"),
            Place(name="Chennai", state="Tamil Nadu", country="India"),
            Place(name="Bangalore", state="Karnataka", country="India"),
            Place(name="Mumbai", state="Maharashtra", country="India"),
            Place(name="Delhi", state="Delhi", country="India"),
            Place(name="Erode", state="Tamil Nadu", country="India")
        ]
        
        for place in places:
            session.add(place)
        
        session.commit()
        print("Database initialized successfully!")
        
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        session.rollback()
    finally:
        session.close()

if __name__ == "__main__":
    init_db() 