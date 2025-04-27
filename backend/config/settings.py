from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "mysql+pymysql://root:password@localhost/epic_x_horoscope"
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ORIGINS: list = ["http://localhost:3000"]
    
    # PDF settings
    PDF_TEMPLATE_DIR: str = "templates"
    PDF_OUTPUT_DIR: str = "output"
    
    class Config:
        env_file = ".env"

settings = Settings()
