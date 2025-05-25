from app.config.database import engine, SessionLocal, get_db

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 