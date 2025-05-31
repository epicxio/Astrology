from pydantic import BaseModel
from typing import Dict, Optional, Any, List
from sqlalchemy import Column, Integer, String, Text
import json

class Predictions(BaseModel):
    career: Optional[str] = None
    health: Optional[str] = None
    relationships: Optional[str] = None
    finance: Optional[str] = None
    bestMatches: Optional[List[str]] = None

class PlanetaryStrength(BaseModel):
    sthana_bala: float
    dig_bala: float
    drik_bala: float
    conjunction: float
    avastha: float
    navamsa: float
    total: float

class HoroscopeBase(BaseModel):
    name: str
    gender: str
    date_of_birth: str
    time_of_birth: str
    place_id: int

class HoroscopeCreate(HoroscopeBase):
    pass

class HoroscopeResponse(HoroscopeBase):
    id: Optional[int] = None
    name: str
    created_at: Optional[str] = None
    date_of_birth: str
    time_of_birth: str
    place_id: int
    place_name: str
    gender: str
    rashi: str
    nakshatra: str
    lagna: str
    planetary_positions: Dict[str, Any]
    predictions: Optional[Dict[str, Any]] = None
    ascendant_long: Optional[float] = None
    rasi_lord: Optional[str] = None
    lagna_lord: Optional[str] = None
    nakshatra_lord: Optional[str] = None
    planetary_strengths: Optional[Dict[str, Any]] = None
    chart_image: Optional[str] = None

    class Config:
        from_attributes = True 