from pydantic import BaseModel
from datetime import date, time, datetime
from typing import Dict, Optional, List

class MatchmakingBase(BaseModel):
    bride_name: str
    bride_dob: date
    bride_tob: time
    bride_place_id: int
    groom_name: str
    groom_dob: date
    groom_tob: time
    groom_place_id: int

class MatchmakingCreate(MatchmakingBase):
    pass

class GunaItem(BaseModel):
    kuta: str
    description: str
    points: float
    max_points: float
    bride_value: str
    groom_value: str

class MatchmakingResponse(BaseModel):
    id: int
    bride_name: str
    bride_dob: date
    bride_tob: time
    bride_place: str
    groom_name: str
    groom_dob: date
    groom_tob: time
    groom_place: str
    guna_score: float
    compatibility: str
    remarks: str
    guna_table: List[GunaItem]
    total_points: float
    max_points: float
    percentage: float
    compatibility_analysis: str
    bride_horoscope: dict
    groom_horoscope: dict
    created_at: datetime
    last_accessed_at: datetime

    class Config:
        from_attributes = True 