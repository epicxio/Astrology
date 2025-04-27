from pydantic import BaseModel
from datetime import date, time
from typing import Dict, Optional

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

    class Config:
        from_attributes = True 