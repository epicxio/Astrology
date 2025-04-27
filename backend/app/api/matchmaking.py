from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

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

        # Calculate matchmaking
        result = MatchMakingCalculator.calculate_compatibility(
            bride_name=input_data.bride_name,
            bride_dob=input_data.bride_dob,
            bride_tob=input_data.bride_tob,
            bride_place_id=input_data.bride_place_id,
            groom_name=input_data.groom_name,
            groom_dob=input_data.groom_dob,
            groom_tob=input_data.groom_tob,
            groom_place_id=input_data.groom_place_id
        )

        # Save to database
        db.add(result)
        db.commit()
        db.refresh(result)

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
            remarks=result.remarks
        )

    except Exception as e:
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
            remarks=result.remarks
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