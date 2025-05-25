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
from ..services.matchmaking_calc import MatchMakingCalculator

router = APIRouter()
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

        return FileResponse(
            path=report,
            filename=f"horoscope_{horoscope_id}.pdf",
            media_type="application/pdf"
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/matchmaking/{matchmaking_id}")
async def get_matchmaking_report(
    matchmaking_id: int,
    language: str = "en",
    db: Session = Depends(get_db)
):
    print(f"DEBUG: Called get_matchmaking_report with id={matchmaking_id}, language={language}")
    try:
        matchmaking = db.query(Matchmaking).filter(Matchmaking.id == matchmaking_id).first()
        print(f"DEBUG: Matchmaking record: {matchmaking}")
        if not matchmaking:
            print("DEBUG: No matchmaking result found")
            raise HTTPException(status_code=404, detail="Matchmaking result not found")

        bride_place = db.query(Place).filter(Place.id == matchmaking.bride_place_id).first()
        groom_place = db.query(Place).filter(Place.id == matchmaking.groom_place_id).first()
        print(f"DEBUG: Bride place: {bride_place} (ID: {matchmaking.bride_place_id}), Groom place: {groom_place} (ID: {matchmaking.groom_place_id})")
        if not bride_place or not groom_place:
            print("DEBUG: Place not found")
            raise HTTPException(status_code=404, detail="Place not found")

        # Recalculate guna_table and related fields for the report
        calc_result = MatchMakingCalculator.calculate_compatibility(
            bride_name=matchmaking.bride_name,
            bride_dob=matchmaking.bride_dob,
            bride_tob=matchmaking.bride_tob,
            bride_place_id=matchmaking.bride_place_id,
            groom_name=matchmaking.groom_name,
            groom_dob=matchmaking.groom_dob,
            groom_tob=matchmaking.groom_tob,
            groom_place_id=matchmaking.groom_place_id,
            db=db
        )

        # Prepare data for PDF generation
        data = {
            "bride_name": matchmaking.bride_name,
            "bride_dob": matchmaking.bride_dob.strftime("%Y-%m-%d"),
            "bride_tob": matchmaking.bride_tob.strftime("%H:%M:%S"),
            "bride_place": bride_place.name,
            "groom_name": matchmaking.groom_name,
            "groom_dob": matchmaking.groom_dob.strftime("%Y-%m-%d"),
            "groom_tob": matchmaking.groom_tob.strftime("%H:%M:%S"),
            "groom_place": groom_place.name,
            "guna_score": float(matchmaking.compatibility_score),
            "compatibility": matchmaking.compatibility,
            # For remarks, use a separate field for Paragraph rendering
            "remarks": matchmaking.remarks,
            # Add Guna Milan data
            "guna_table": calc_result.get("guna_table", []),
            "total_points": calc_result.get("total_points", 0),
            "max_points": calc_result.get("max_points", 0),
            "percentage": calc_result.get("percentage", 0),
            "compatibility_analysis": calc_result.get("compatibility_analysis", "")
        }

        print(f"DEBUG: PDF data: {data}")

        # Generate PDF
        report = pdf_generator.generate_matchmaking_pdf(data, language)
        print(f"DEBUG: PDF generated at {report}")

        # Return the file
        return FileResponse(
            path=report,
            filename=f"matchmaking_{matchmaking_id}.pdf",
            media_type="application/pdf"
        )

    except Exception as e:
        print(f"DEBUG: Exception occurred: {e}")
        raise HTTPException(status_code=500, detail=str(e)) 