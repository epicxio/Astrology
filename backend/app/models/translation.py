from sqlalchemy import Column, String, Text, UniqueConstraint
from .base import BaseModel

class Translation(BaseModel):
    __tablename__ = "translations"

    language = Column(String(10), nullable=False)
    key = Column(String(255), nullable=False)
    value = Column(Text, nullable=False)

    __table_args__ = (
        UniqueConstraint('language', 'key', name='uix_language_key'),
    )

    def __repr__(self):
        return f"<Translation {self.key} ({self.language})>" 