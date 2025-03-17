from typing import Any, List
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from app.db.session import get_db

from app import crud
from app import schemas
from app.schemas import location

router = APIRouter()

@router.get("/states/", response_model=List[schemas.StateSchema]) 
def get_all_states(db: Session = Depends(get_db)):
    return crud.crud_location.get_all_states(db)


@router.post("/cities/", response_model=dict)
def get_cities_by_state(*, db: Session = Depends(get_db), params: schemas.Cities):
    """Fetch all cities under a given state using query params"""
    try:
        cities = crud.crud_location.get_cities_by_state(db, params)
        if not cities:
            return JSONResponse(content={"success": False, "message": "No cities found"}, status_code=404)
        city_data = [schemas.CitySchema.model_validate(city).model_dump() for city in cities]
        return {"success": True, "Cities": city_data}
    except Exception as e:
        return JSONResponse(status_code=400, content={'success': False, 'message': str(e)})
