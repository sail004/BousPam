from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils, luhn
from services.schemas.place import place_request, place_response
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


place_router = APIRouter(prefix='/place', tags=['Interaction with places'])


@place_router.get(
    "/getlist/",
    response_model=list[place_response.ReturnPlace],
    description="Operation for getting list of all places"
)
async def read_places(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    places = await crud_utils.get_places(db, skip=skip, limit=limit)
    return places


@place_router.get(
    "/get/by-name/",
    response_model=place_response.ReturnPlace,
    description="Operation for getting place by its name"
)
async def read_place(name: str, db: Session = Depends(get_db)):
    place = await crud_utils.get_place_by_name(db, name=name)
    if place is None:
        raise HTTPException(status_code=404, detail=f"Place with name=\'{name}\' not found")
    return place


@place_router.post(
    "/create/",
    response_model=place_response.ReturnPlace,
    description="Operation for creating place"
)
async def create_place(place: place_request.PlaceCreate, db: Session = Depends(get_db)):
    place_exists = await crud_utils.get_place_by_name(db, name=place.name)
    if place_exists:
        raise HTTPException(status_code=409, detail=f"The place with name=\'{place.name}\' has already been created")
    return await crud_utils.create_place(db=db, place=place)


@place_router.put(
    "/update/by-id/",
    response_model=place_response.ReturnPlace,
    description="Operation for updating place by its id"
)
async def update_place_by_id(place_id: int, place: place_request.PlaceUpdate, db: Session = Depends(get_db)):
    db_place = await crud_utils.get_place_by_id(db, place_id=place_id)
    if db_place is None:
        raise HTTPException(status_code=404, detail=f"Place with id=\'{place_id}\' not found")
    return await crud_utils.update_place(db, place=place, place_id=place_id)


@place_router.put(
    "/update/by-name/",
    response_model=place_response.ReturnPlace,
    description="Operation for updating place by its name"
)
async def update_place_by_name(name: str, place: place_request.PlaceUpdate, db: Session = Depends(get_db)):
    db_place = await crud_utils.get_place_by_name(db, name=name)
    if db_place is None:
        raise HTTPException(status_code=404, detail=f"Place with name=\'{name}\' not found")
    return await crud_utils.update_place(db, place=place, place_id=db_place.place_id)


@place_router.put(
    "/update/status/",
    response_model=place_response.ReturnPlace,
    description="Operation for updating place status by its name"
)
async def update_place_by_name(name: str, status: str, db: Session = Depends(get_db)):
    if status not in ['active', 'inactive']:
        raise HTTPException(status_code=400, detail=f"Incorrect status, status must be one of 'active', 'inactive'")
    db_place = await crud_utils.get_place_by_name(db, name=name)
    if db_place is None:
        raise HTTPException(status_code=404, detail=f"Place with name=\'{name}\' not found")
    return await crud_utils.update_place_status(db, status=status, name=name)
