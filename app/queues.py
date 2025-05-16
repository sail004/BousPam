from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils, luhn
from services.schemas.queue import queue_request, queue_response
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


queue_router = APIRouter(prefix='/queue', tags=['Interaction with queues'])


@queue_router.get(
    "/getlist/free/",
    response_model=list[queue_response.ReturnQueue],
    description="Operation for getting list of all free places in queue"
)
async def read_free_queues(place_name: str, date: datetime, db: Session = Depends(get_db)):
    queues = await crud_utils.get_free_queues(db, place_name, date)
    return queues


@queue_router.get(
    "/getlist/occupied/",
    response_model=list[queue_response.ReturnQueue],
    description="Operation for getting list of all occupied places in queue"
)
async def read_occupied_queues(place_name: str, date: datetime, db: Session = Depends(get_db)):
    queues = await crud_utils.get_occupied_queues(db, place_name, date)
    return queues


@queue_router.put(
    "/occupy-place/",
    response_model=list[queue_response.ReturnQueue],
    description="Operation for occupy place in queue"
)
async def occupy_place_in_queue(place: queue_request.OccupyPlaceInQueue, db: Session = Depends(get_db)):
    status = await crud_utils.occupy_place_in_queue(db=db, place_info=place)
    return queue_response.Message(msg=status)
