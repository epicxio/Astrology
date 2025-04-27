from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import BaseModel

class Place(BaseModel):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timezone = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    horoscopes = relationship("Horoscope", back_populates="place")

    def __repr__(self):
        return f"<Place {self.name}>" 