from pydantic import BaseModel
from typing import Optional

class TranslationBase(BaseModel):
    language: str
    key: str
    value: str

class TranslationCreate(TranslationBase):
    pass

class Translation(TranslationBase):
    id: int

    class Config:
        from_attributes = True 