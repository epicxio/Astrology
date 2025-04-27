from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.translation import Translation as TranslationModel
from ..schemas.translation import Translation, TranslationCreate
from ..config.database import get_db

router = APIRouter(prefix="/api/translations")

@router.get("", response_model=List[Translation])
async def get_translations(
    language: Optional[str] = None,
    key: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get translations filtered by language and/or key."""
    try:
        query = db.query(TranslationModel)
        if language:
            query = query.filter(TranslationModel.language == language)
        if key:
            query = query.filter(TranslationModel.key == key)
        translations = query.all()
        return translations
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=Translation)
async def get_translation(id: int, db: Session = Depends(get_db)):
    """Get a specific translation by ID."""
    try:
        translation = db.query(TranslationModel).filter(TranslationModel.id == id).first()
        if not translation:
            raise HTTPException(status_code=404, detail="Translation not found")
        return translation
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 