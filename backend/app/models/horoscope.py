from sqlalchemy import Column, Integer, String, Date, Time, ForeignKey, DateTime, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from .base import BaseModel

class Horoscope(BaseModel):
    __tablename__ = "horoscopes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    gender = Column(String(1), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    time_of_birth = Column(Time, nullable=False)
    place_id = Column(Integer, ForeignKey("places.id"), nullable=False)
    rashi = Column(String(20), nullable=False)
    nakshatra = Column(String(20), nullable=False)
    lagna = Column(String(20), nullable=False)
    planetary_positions = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    place = relationship("Place", back_populates="horoscopes")

    def __repr__(self):
        return f"<Horoscope {self.name} ({self.rashi})>" 