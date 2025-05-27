from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import traceback
import sys

from ..models.matchmaking import Matchmaking
from ..models.place import Place
from ..schemas.matchmaking import MatchmakingCreate, MatchmakingResponse
from ..services.matchmaking_calc import MatchMakingCalculator
from ..config.database import get_db

router = APIRouter(prefix="/api/matchmaking")

@router.post("/calculate", response_model=MatchmakingResponse)
async def calculate_matchmaking(
    input_data: MatchmakingCreate,
    db: Session = Depends(get_db)
):
    """Calculate matchmaking compatibility based on input data."""
    try:
        # Verify places exist
        bride_place = db.query(Place).filter(Place.id == input_data.bride_place_id).first()
        groom_place = db.query(Place).filter(Place.id == input_data.groom_place_id).first()
        if not bride_place or not groom_place:
            raise HTTPException(status_code=404, detail="Place not found")

        print("bride_place_id:", input_data.bride_place_id)
        print("groom_place_id:", input_data.groom_place_id)

        # Calculate matchmaking (get detailed result)
        result = MatchMakingCalculator.calculate_compatibility(
            bride_name=input_data.bride_name,
            bride_dob=input_data.bride_dob,
            bride_tob=input_data.bride_tob,
            bride_place_id=input_data.bride_place_id,
            groom_name=input_data.groom_name,
            groom_dob=input_data.groom_dob,
            groom_tob=input_data.groom_tob,
            groom_place_id=input_data.groom_place_id,
            db=db
        )

        # Check for duplicate records
        existing_result = db.query(Matchmaking).filter(
            Matchmaking.bride_name == input_data.bride_name,
            Matchmaking.bride_dob == input_data.bride_dob,
            Matchmaking.bride_tob == input_data.bride_tob,
            Matchmaking.bride_place_id == input_data.bride_place_id,
            Matchmaking.groom_name == input_data.groom_name,
            Matchmaking.groom_dob == input_data.groom_dob,
            Matchmaking.groom_tob == input_data.groom_tob,
            Matchmaking.groom_place_id == input_data.groom_place_id
        ).first()

        if existing_result:
            # Return existing result instead of creating a new one
            response = MatchmakingResponse(
                id=existing_result.id,
                bride_name=existing_result.bride_name,
                bride_dob=existing_result.bride_dob,
                bride_tob=existing_result.bride_tob,
                bride_place=bride_place.name,
                groom_name=existing_result.groom_name,
                groom_dob=existing_result.groom_dob,
                groom_tob=existing_result.groom_tob,
                groom_place=groom_place.name,
                guna_score=float(existing_result.compatibility_score),
                compatibility=existing_result.compatibility,
                remarks=existing_result.remarks,
                guna_table=result["guna_table"],  # Use fresh calculation for detailed data
                total_points=result["total_points"],
                max_points=result["max_points"],
                percentage=result["percentage"],
                compatibility_analysis=result["compatibility_analysis"],
                bride_horoscope=result.get("bride_horoscope", {}),
                groom_horoscope=result.get("groom_horoscope", {}),
                created_at=existing_result.created_at,
                last_accessed_at=existing_result.last_accessed_at
            )
            print('DEBUG: Returning existing result with ID:', existing_result.id)
            return response

        # Save the result to the database if no duplicate found
        new_result = Matchmaking(
            bride_name=input_data.bride_name,
            bride_dob=input_data.bride_dob,
            bride_tob=input_data.bride_tob,
            bride_place_id=input_data.bride_place_id,
            groom_name=input_data.groom_name,
            groom_dob=input_data.groom_dob,
            groom_tob=input_data.groom_tob,
            groom_place_id=input_data.groom_place_id,
            compatibility_score=result["total_points"],
            compatibility="Ashtakoota Match",
            remarks=result["compatibility_analysis"]
        )
        db.add(new_result)
        db.commit()
        db.refresh(new_result)

        response = MatchmakingResponse(
            id=new_result.id,
            bride_name=input_data.bride_name,
            bride_dob=input_data.bride_dob,
            bride_tob=input_data.bride_tob,
            bride_place=bride_place.name,
            groom_name=input_data.groom_name,
            groom_dob=input_data.groom_dob,
            groom_tob=input_data.groom_tob,
            groom_place=groom_place.name,
            guna_score=result["total_points"],
            compatibility="Ashtakoota Match",
            remarks=result["compatibility_analysis"],
            guna_table=result["guna_table"],
            total_points=result["total_points"],
            max_points=result["max_points"],
            percentage=result["percentage"],
            compatibility_analysis=result["compatibility_analysis"],
            bride_horoscope=result.get("bride_horoscope", {}),
            groom_horoscope=result.get("groom_horoscope", {}),
            created_at=new_result.created_at,
            last_accessed_at=new_result.last_accessed_at
        )
        import json
        print('DEBUG: API response =', response.json())
        return response

    except Exception as e:
        print("==== Exception in /api/matchmaking/calculate ====")
        print("Request data:", input_data)
        traceback.print_exc(file=sys.stdout)
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{matchmaking_id}", response_model=MatchmakingResponse)
async def get_matchmaking(
    matchmaking_id: int,
    db: Session = Depends(get_db)
):
    """Get a specific matchmaking result by ID."""
    try:
        result = db.query(Matchmaking).filter(Matchmaking.id == matchmaking_id).first()
        if not result:
            raise HTTPException(status_code=404, detail="Matchmaking result not found")

        bride_place = db.query(Place).filter(Place.id == result.bride_place_id).first()
        groom_place = db.query(Place).filter(Place.id == result.groom_place_id).first()

        return MatchmakingResponse(
            id=result.id,
            bride_name=result.bride_name,
            bride_dob=result.bride_dob,
            bride_tob=result.bride_tob,
            bride_place=bride_place.name,
            groom_name=result.groom_name,
            groom_dob=result.groom_dob,
            groom_tob=result.groom_tob,
            groom_place=groom_place.name,
            guna_score=float(result.compatibility_score),
            compatibility=result.compatibility,
            remarks=result.remarks,
            created_at=result.created_at,
            last_accessed_at=result.last_accessed_at
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/places", response_model=List[str])
async def get_places():
    try:
        # TODO: Implement getting places from database
        return []
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[MatchmakingResponse])
async def list_matchmakings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    results = db.query(Matchmaking).offset(skip).limit(limit).all()
    response = []
    for result in results:
        bride_place = db.query(Place).filter(Place.id == result.bride_place_id).first()
        groom_place = db.query(Place).filter(Place.id == result.groom_place_id).first()
        # Recalculate guna_table and related fields for each record
        calc_result = MatchMakingCalculator.calculate_compatibility(
            bride_name=result.bride_name,
            bride_dob=result.bride_dob,
            bride_tob=result.bride_tob,
            bride_place_id=result.bride_place_id,
            groom_name=result.groom_name,
            groom_dob=result.groom_dob,
            groom_tob=result.groom_tob,
            groom_place_id=result.groom_place_id,
            db=db
        )
        response.append(MatchmakingResponse(
            id=result.id,
            bride_name=result.bride_name,
            bride_dob=result.bride_dob,
            bride_tob=result.bride_tob,
            bride_place=bride_place.name if bride_place else None,
            groom_name=result.groom_name,
            groom_dob=result.groom_dob,
            groom_tob=result.groom_tob,
            groom_place=groom_place.name if groom_place else None,
            guna_score=float(result.compatibility_score),
            compatibility=result.compatibility,
            remarks=result.remarks,
            guna_table=calc_result.get("guna_table", []),
            total_points=calc_result.get("total_points", 0),
            max_points=calc_result.get("max_points", 0),
            percentage=calc_result.get("percentage", 0),
            compatibility_analysis=calc_result.get("compatibility_analysis", ""),
            bride_horoscope=calc_result.get("bride_horoscope", {}),
            groom_horoscope=calc_result.get("groom_horoscope", {}),
            created_at=result.created_at,
            last_accessed_at=result.last_accessed_at
        ))
    return response 