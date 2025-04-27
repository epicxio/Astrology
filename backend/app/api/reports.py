from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import FileResponse
from typing import Optional
from sqlalchemy.orm import Session
import os
from datetime import datetime

from ..models.horoscope import Horoscope
from ..models.matchmaking import Matchmaking
from ..models.place import Place
from ..services.pdf_generator import PDFGenerator
from ..config.database import get_db

router = APIRouter(prefix="/api/reports")
pdf_generator = PDFGenerator()

@router.get("/horoscope/{horoscope_id}")
async def get_horoscope_report(
    horoscope_id: int,
    language: str = "en",
    db: Session = Depends(get_db)
):
    """Generate and return a horoscope report PDF."""
    try:
        horoscope = db.query(Horoscope).filter(Horoscope.id == horoscope_id).first()
        if not horoscope:
            raise HTTPException(status_code=404, detail="Horoscope not found")

        place = db.query(Place).filter(Place.id == horoscope.place_id).first()
        if not place:
            raise HTTPException(status_code=404, detail="Place not found")

        report = pdf_generator.generate_horoscope_report(
            horoscope=horoscope,
            place=place,
            language=language
        )

        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/matchmaking/{matchmaking_id}")
async def get_matchmaking_report(
    matchmaking_id: int,
    language: str = "en",
    db: Session = Depends(get_db)
):
    """Generate and return a matchmaking report PDF."""
    try:
        matchmaking = db.query(Matchmaking).filter(Matchmaking.id == matchmaking_id).first()
        if not matchmaking:
            raise HTTPException(status_code=404, detail="Matchmaking result not found")

        bride_place = db.query(Place).filter(Place.id == matchmaking.bride_place_id).first()
        groom_place = db.query(Place).filter(Place.id == matchmaking.groom_place_id).first()
        if not bride_place or not groom_place:
            raise HTTPException(status_code=404, detail="Place not found")

        report = pdf_generator.generate_matchmaking_report(
            matchmaking=matchmaking,
            bride_place=bride_place,
            groom_place=groom_place,
            language=language
        )

        return report

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 