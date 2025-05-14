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
    "/getlist/",
    response_model=list[queue_response.ReturnOperation],
    description="Operation for getting list of all operations"
)
async def read_operations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    operations = await crud_utils.get_operations(db, skip=skip, limit=limit)
    return operations
