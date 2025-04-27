from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Database settings
    DATABASE_URL: str = "mysql+pymysql://root:@localhost/epic_x_horoscope"
    
    # JWT settings
    SECRET_KEY: str = "your-secret-key-here"  # Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Application settings
    DEBUG: bool = True
    API_V1_STR: str = "/api/v1"
    
    model_config = SettingsConfigDict(case_sensitive=True)

settings = Settings() 