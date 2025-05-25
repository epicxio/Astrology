from sqlalchemy import Column, String, ForeignKey, Numeric, Date, Time, DateTime
from sqlalchemy.orm import relationship
from .base import BaseModel
from datetime import datetime

class Matchmaking(BaseModel):
    __tablename__ = "matchmaking_results"

    bride_name = Column(String(100), nullable=False)
    bride_dob = Column(Date, nullable=False)
    bride_tob = Column(Time, nullable=False)
    bride_place_id = Column(ForeignKey("places.id"), nullable=False)
    
    groom_name = Column(String(100), nullable=False)
    groom_dob = Column(Date, nullable=False)
    groom_tob = Column(Time, nullable=False)
    groom_place_id = Column(ForeignKey("places.id"), nullable=False)
    
    compatibility_score = Column(Numeric(5, 2), nullable=False)
    compatibility = Column(String(50), nullable=False)
    remarks = Column(String(500), nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_accessed_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    bride_place = relationship("Place", foreign_keys=[bride_place_id])
    groom_place = relationship("Place", foreign_keys=[groom_place_id])

    def __repr__(self):
        return f"<Matchmaking {self.bride_name} & {self.groom_name}>" 