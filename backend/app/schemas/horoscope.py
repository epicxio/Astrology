from pydantic import BaseModel
from typing import Dict, Optional, Any, List

class Predictions(BaseModel):
    career: Optional[str] = None
    health: Optional[str] = None
    relationships: Optional[str] = None
    finance: Optional[str] = None
    bestMatches: Optional[List[str]] = None

class HoroscopeBase(BaseModel):
    name: str
    gender: str
    date_of_birth: str
    time_of_birth: str
    place_id: int

class HoroscopeCreate(HoroscopeBase):
    pass

class HoroscopeResponse(HoroscopeBase):
    id: int
    created_at: str
    updated_at: Optional[str] = None
    rashi: str
    nakshatra: str
    lagna: str
    planetary_positions: Dict[str, Any]
    place_name: str
    predictions: Optional[Predictions] = None
    ascendant_long: Optional[float] = None
    rasi_lord: Optional[str] = None
    lagna_lord: Optional[str] = None
    nakshatra_lord: Optional[str] = None

    class Config:
        from_attributes = True 