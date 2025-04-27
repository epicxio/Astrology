from pydantic import BaseModel
from typing import Optional

class PlaceBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    timezone: str

class PlaceCreate(PlaceBase):
    pass

class PlaceResponse(PlaceBase):
    id: int

    class Config:
        from_attributes = True 