from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
import logging
from ..models.place import Place
from ..schemas.place import PlaceResponse
from ..db.session import get_db

# Initialize router
router = APIRouter(tags=["places"])

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.get("", response_model=List[PlaceResponse])  # Route without trailing slash
async def get_places(db: Session = Depends(get_db)):
    """Get all places."""
    try:
        logger.info("Attempting to fetch places from database")
        places = db.query(Place).all()
        logger.info(f"Successfully fetched {len(places)} places")
        return places
    except Exception as e:
        logger.error(f"Error fetching places: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching places: {str(e)}")

@router.get("/{place_id}", response_model=PlaceResponse)
async def get_place(place_id: int, db: Session = Depends(get_db)):
    """Get a specific place by ID."""
    try:
        logger.info(f"Attempting to fetch place with ID: {place_id}")
        place = db.query(Place).filter(Place.id == place_id).first()
        
        if not place:
            logger.error(f"Place with ID {place_id} not found")
            raise HTTPException(status_code=404, detail="Place not found")
            
        logger.info(f"Successfully found place: {place.name}")
        return place
    except Exception as e:
        logger.error(f"Error fetching place: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error fetching place: {str(e)}") 