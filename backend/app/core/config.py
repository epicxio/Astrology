import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Epic-X Horoscope"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api"
    DESCRIPTION: str = "API for horoscope calculations and matchmaking"
    CORS_ORIGINS: list = ["*"]
    
    # Database settings
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "")
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT: str = os.getenv("MYSQL_PORT", "3306")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "epic_x_horoscope")
    
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

settings = Settings() 