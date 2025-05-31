from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional, Any, Dict
from ..db.session import get_db
from ..schemas.horoscope import HoroscopeCreate, HoroscopeResponse
from ..services.horoscope_calculator import calculate_horoscope
from ..models.horoscope import Horoscope
from ..models.place import Place
from datetime import datetime, date, time
import json
import traceback
from pydantic import BaseModel
import swisseph as swe
import pytz
from fastapi.responses import FileResponse
from app.services.horoscope_chart import plot_planetary_positions, plot_south_indian_chart
import os
import logging
from sqlalchemy import Column, Text

router = APIRouter()

class Predictions(BaseModel):
    career: Optional[str] = None
    health: Optional[str] = None
    relationships: Optional[str] = None
    finance: Optional[str] = None
    bestMatches: Optional[List[str]] = None

def parse_time_string(time_str):
    for fmt in ("%H:%M:%S", "%H:%M"):
        try:
            return datetime.strptime(time_str, fmt).time()
        except ValueError:
            continue
    raise ValueError(f"Invalid time format: {time_str}")

@router.post("/", response_model=HoroscopeResponse)
@router.post("/calculate", response_model=HoroscopeResponse)
async def create_horoscope(horoscope: HoroscopeCreate, db: Session = Depends(get_db)):
    """Create a new horoscope calculation and save it to the SQLite horoscopes table."""
    try:
        # Parse date and time
        try:
            if isinstance(horoscope.date_of_birth, str):
                date_of_birth = datetime.strptime(horoscope.date_of_birth, "%Y-%m-%d").date()
            elif isinstance(horoscope.date_of_birth, date):
                date_of_birth = horoscope.date_of_birth
            else:
                raise ValueError("Invalid date_of_birth type")

            if isinstance(horoscope.time_of_birth, str):
                time_of_birth = parse_time_string(horoscope.time_of_birth)
            elif isinstance(horoscope.time_of_birth, time):
                time_of_birth = horoscope.time_of_birth
            else:
                raise ValueError("Invalid time_of_birth type")
        except ValueError as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "common.errorCalculatingHoroscope",
                    "message": f"Invalid date/time format: {str(e)}",
                    "step": "parsing_date_time",
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "traceback": traceback.format_exc(),
                }
            )
        
        # Normalize gender
        gender = horoscope.gender.strip().lower()
        if gender in ["male", "m"]:
            gender = "M"
        elif gender in ["female", "f"]:
            gender = "F"
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "horoscope.calculationError",
                    "message": "Gender must be 'M', 'F', 'Male', or 'Female'",
                    "step": "normalizing_gender",
                    "exception_type": "ValueError",
                    "exception_message": "Invalid gender value",
                    "traceback": traceback.format_exc(),
                }
            )
        
        # Get place details
        try:
            place = db.query(Place).filter(Place.id == horoscope.place_id).first()
            if not place:
                raise ValueError("Place not found")
        except Exception as e:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "common.errorCalculatingHoroscope",
                    "message": "Place not found",
                    "step": "fetching_place",
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "traceback": traceback.format_exc(),
                }
            )
        
        try:
            # Calculate horoscope
            swe.set_sid_mode(swe.SIDM_LAHIRI)
            horoscope_data = calculate_horoscope(
                date_of_birth=date_of_birth,
                time_of_birth=time_of_birth,
                latitude=place.latitude,
                longitude=place.longitude,
                timezone=place.timezone,
                gender=gender
            )
            predictions = Predictions(
                career="Favorable time for career growth",
                health="Take care of your physical well-being",
                relationships="Strong bonds will be formed",
                finance="Good period for investments",
                bestMatches=["Mesha", "Vrishabha", "Mithuna"]
            )
            # Debug logging for calculation
            dt_naive = datetime.combine(date_of_birth, time_of_birth)
            tz = place.timezone
            print(f"Local time: {dt_naive} ({tz})")
            # Use pytz to get UTC time
            dt_local = pytz.timezone(tz).localize(dt_naive)
            dt_utc = dt_local.astimezone(pytz.utc)
            print(f"UTC time: {dt_utc}")
            print(f"Julian Day UT: {swe.julday(dt_utc.year, dt_utc.month, dt_utc.day, dt_utc.hour + dt_utc.minute/60 + dt_utc.second/3600)}")
            print(f"Latitude: {place.latitude}, Longitude: {place.longitude}")
            print(f"Ascendant longitude: {horoscope_data['ascendant_long']}")
            print(f"Lagna index: {int(horoscope_data['ascendant_long'] // 30) % 12}, Lagna: {horoscope_data['lagna']}")

            # Generate and save South Indian Style Rasi Chart
            planetary_positions = horoscope_data['planetary_positions']
            birth_details = [
                date_of_birth.strftime("%d - %B - %Y"),
                time_of_birth.strftime("%H : %M : %S"),
                "Rasi", horoscope_data['rashi'],
                horoscope_data['nakshatra']
            ]
            chart_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "horoscope_charts")
            os.makedirs(chart_folder, exist_ok=True)
            chart_filename = f"south_indian_chart_{datetime.now().strftime('%Y%m%d%H%M%S')}_{horoscope.name}.png"
            chart_path = os.path.join(chart_folder, chart_filename)
            try:
                plot_south_indian_chart(planetary_positions, filename=chart_path, birth_details=birth_details)
            except Exception as chart_exc:
                logging.error(f"Failed to generate or save chart: {chart_exc}")
                chart_path = None

        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "horoscope.calculationError",
                    "message": f"Error during horoscope calculation: {str(e)}",
                    "step": "horoscope_calculation",
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "traceback": traceback.format_exc(),
                }
            )
        
        try:
            # Create horoscope record
            db_horoscope = Horoscope(
                name=horoscope.name,
                date_of_birth=date_of_birth,
                time_of_birth=time_of_birth,
                place_id=horoscope.place_id,
                gender=gender,
                rashi=horoscope_data['rashi'],
                nakshatra=horoscope_data['nakshatra'],
                lagna=horoscope_data['lagna'],
                planetary_positions=json.dumps(horoscope_data['planetary_positions']),
                planetary_strengths=json.dumps(horoscope_data['planetary_strengths']),
                chart_image=chart_path
            )
            db.add(db_horoscope)
            db.commit()
            db.refresh(db_horoscope)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "common.errorCalculatingHoroscope",
                    "message": f"Error saving horoscope to database: {str(e)}",
                    "step": "saving_to_database",
                    "exception_type": type(e).__name__,
                    "exception_message": str(e),
                    "traceback": traceback.format_exc(),
                }
            )
        
        return HoroscopeResponse(
            id=db_horoscope.id,
            name=db_horoscope.name,
            created_at=db_horoscope.created_at.isoformat(),
            date_of_birth=db_horoscope.date_of_birth.isoformat(),
            time_of_birth=db_horoscope.time_of_birth.isoformat(),
            place_id=db_horoscope.place_id,
            place_name=place.name,
            gender=db_horoscope.gender,
            rashi=db_horoscope.rashi,
            nakshatra=db_horoscope.nakshatra,
            lagna=db_horoscope.lagna,
            planetary_positions=json.loads(db_horoscope.planetary_positions),
            planetary_strengths=json.loads(db_horoscope.planetary_strengths) if db_horoscope.planetary_strengths else None,
            predictions=predictions.dict(),
            ascendant_long=horoscope_data.get('ascendant_long'),
            rasi_lord=horoscope_data.get('rasi_lord'),
            lagna_lord=horoscope_data.get('lagna_lord'),
            nakshatra_lord=horoscope_data.get('nakshatra_lord'),
            chart_image=db_horoscope.chart_image
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail={
                "error": "common.errorCalculatingHoroscope",
                "message": f"An unexpected error occurred: {str(e)}",
                "step": "unknown",
                "exception_type": type(e).__name__,
                "exception_message": str(e),
                "traceback": traceback.format_exc(),
            }
        )

@router.get("/{horoscope_id}", response_model=HoroscopeResponse)
async def get_horoscope(horoscope_id: int, db: Session = Depends(get_db)):
    horoscope = db.query(Horoscope).filter(Horoscope.id == horoscope_id).first()
    if not horoscope:
        raise HTTPException(status_code=404, detail="Horoscope not found")
    
    place = db.query(Place).filter(Place.id == horoscope.place_id).first()
    if not place:
        raise HTTPException(status_code=404, detail="Place not found")
    
    predictions = Predictions(
        career="Favorable time for career growth",
        health="Take care of your physical well-being",
        relationships="Strong bonds will be formed",
        finance="Good period for investments",
        bestMatches=["Mesha", "Vrishabha", "Mithuna"]
    )
    planetary_strengths = horoscope.planetary_strengths
    if isinstance(planetary_strengths, str):
        try:
            planetary_strengths = json.loads(planetary_strengths)
        except Exception:
            planetary_strengths = None
    return HoroscopeResponse(
        id=horoscope.id,
        name=horoscope.name,
        created_at=horoscope.created_at.isoformat(),
        date_of_birth=horoscope.date_of_birth.isoformat(),
        time_of_birth=horoscope.time_of_birth.isoformat(),
        place_id=horoscope.place_id,
        place_name=place.name,
        gender=horoscope.gender,
        rashi=horoscope.rashi,
        nakshatra=horoscope.nakshatra,
        lagna=horoscope.lagna,
        planetary_positions=json.loads(horoscope.planetary_positions),
        planetary_strengths=planetary_strengths,
        predictions=predictions.dict(),
        chart_image=horoscope.chart_image
    )

@router.get("/", response_model=List[HoroscopeResponse])
async def list_horoscopes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    horoscopes = db.query(Horoscope).offset(skip).limit(limit).all()
    results = []
    for horoscope in horoscopes:
        place = db.query(Place).filter(Place.id == horoscope.place_id).first()
        if place:
            predictions = Predictions(
                career="Favorable time for career growth",
                health="Take care of your physical well-being",
                relationships="Strong bonds will be formed",
                finance="Good period for investments",
                bestMatches=["Mesha", "Vrishabha", "Mithuna"]
            )
            # Always include planetary_positions as a dict
            planetary_positions = horoscope.planetary_positions
            if isinstance(planetary_positions, str):
                try:
                    planetary_positions = json.loads(planetary_positions)
                except Exception:
                    planetary_positions = {}
            planetary_strengths = horoscope.planetary_strengths
            if isinstance(planetary_strengths, str):
                try:
                    planetary_strengths = json.loads(planetary_strengths)
                except Exception:
                    planetary_strengths = None
            results.append(HoroscopeResponse(
                id=horoscope.id,
                name=horoscope.name,
                created_at=horoscope.created_at.isoformat(),
                date_of_birth=horoscope.date_of_birth.isoformat(),
                time_of_birth=horoscope.time_of_birth.isoformat(),
                place_id=horoscope.place_id,
                place_name=place.name,
                gender=horoscope.gender,
                rashi=horoscope.rashi,
                nakshatra=horoscope.nakshatra,
                lagna=horoscope.lagna,
                planetary_positions=planetary_positions,
                planetary_strengths=planetary_strengths,
                predictions=predictions.dict(),
                chart_image=horoscope.chart_image
            ))
    return results

@router.get("/chart/{horoscope_id}")
async def get_horoscope_chart(horoscope_id: int, db: Session = Depends(get_db)):
    horoscope = db.query(Horoscope).filter(Horoscope.id == horoscope_id).first()
    if not horoscope:
        raise HTTPException(status_code=404, detail="Horoscope not found")
    # Parse planetary_positions from JSON if needed
    if isinstance(horoscope.planetary_positions, str):
        planetary_positions = json.loads(horoscope.planetary_positions)
    else:
        planetary_positions = horoscope.planetary_positions
    # Always use static/horoscope_charts for chart storage
    chart_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "horoscope_charts")
    os.makedirs(chart_folder, exist_ok=True)
    filename = f"horoscope_chart_{horoscope_id}.png"
    filepath = os.path.join(chart_folder, filename)
    # Only generate if it doesn't exist
    if not os.path.exists(filepath):
        plot_planetary_positions(planetary_positions, filename=filepath)
    return FileResponse(filepath, media_type="image/png", filename=filename)

@router.get("/chart/south/{horoscope_id}")
async def get_south_indian_chart(horoscope_id: int, db: Session = Depends(get_db)):
    horoscope = db.query(Horoscope).filter(Horoscope.id == horoscope_id).first()
    if not horoscope:
        raise HTTPException(status_code=404, detail="Horoscope not found")
    # Parse planetary_positions from JSON if needed
    if isinstance(horoscope.planetary_positions, str):
        planetary_positions = json.loads(horoscope.planetary_positions)
    else:
        planetary_positions = horoscope.planetary_positions
    # Prepare birth details for center box
    birth_details = [
        horoscope.date_of_birth.strftime("%d - %B - %Y") if hasattr(horoscope.date_of_birth, 'strftime') else str(horoscope.date_of_birth),
        horoscope.time_of_birth.strftime("%H : %M : %S") if hasattr(horoscope.time_of_birth, 'strftime') else str(horoscope.time_of_birth),
        f"Rasi", horoscope.rashi,
        horoscope.nakshatra
    ]
    # Always use static/horoscope_charts for chart storage
    chart_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "horoscope_charts")
    os.makedirs(chart_folder, exist_ok=True)
    filename = f"south_indian_chart_{horoscope_id}.png"
    filepath = os.path.join(chart_folder, filename)
    # Only generate if it doesn't exist
    if not os.path.exists(filepath):
        plot_south_indian_chart(planetary_positions, filename=filepath, birth_details=birth_details)
    return FileResponse(filepath, media_type="image/png", filename=filename) 