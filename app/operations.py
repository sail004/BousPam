from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
import os
import crud_utils
import models
import schemas
from crud_utils import add_to_stoplist
from database import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


operations_router = APIRouter(prefix='/operations', tags=['Работа с операциями'])


@operations_router.get("/getlist/") #, response_model=List[schemas.Product]
def read_operations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    operations = crud_utils.get_operations(db, skip=skip, limit=limit)
    return operations


@operations_router.get("/get/by-terminal-id/") #, response_model=schemas.Product
def read_operations_by_terminal_id(terminal_id: int, db: Session = Depends(get_db)):
    db_ops = crud_utils.get_operations_by_terminal_id(db, term_id=terminal_id)
    if db_ops is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    return db_ops


@operations_router.get("/get/by-user-id/") #, response_model=schemas.Product
def read_operations_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_ops = crud_utils.get_operations_by_user_id(db, user_id=user_id)
    if db_ops is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return db_ops


@operations_router.put("/payment/") #, response_model=schemas.Product
def payment_by_user_id(operation: schemas.OperationPaymentCreate, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=operation.id_user)
    db_terminal = crud_utils.get_terminal_by_id(db, terminal_id=operation.id_terminal)
    if db_terminal is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{operation.id_terminal}\' not found")
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{operation.id_user}\' not found")
    if db_terminal.hash != operation.terminal_hash:
        raise HTTPException(status_code=404, detail=f"Incorrect terminal hash")
    delta_time = datetime.now() - operation.request_time.replace(tzinfo=None)
    #crud_utils.create_operation_payment(db, operation, 'payment')
    balance_change = crud_utils.get_price_by_terminal_id(db, operation.id_terminal)
    if delta_time < timedelta(minutes=1):
        if db_user.balance < abs(balance_change):
            raise HTTPException(status_code=400, detail=f"Insufficient funds to make the payment")
    new_balance = crud_utils.create_operation_payment(db, operation, 'payment')
    if new_balance < 0:
        add_to_stoplist(db, schemas.StopListCreate(
            card_number=db_user.card_number,
            owner_id=db_user.id,
            owner_phone_number=db_user.phone_number
        ))
    return new_balance


@operations_router.put("/replenishment/") #, response_model=schemas.Product
def replenishment_by_user_id(operation: schemas.OperationReplenishmentCreate, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=operation.id_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{operation.id_user}\' not found")
    new_balance = crud_utils.create_operation_replenishment(db, operation, 'replenishment')
    if new_balance > 0 and crud_utils.is_in_stoplist(db, db_user.card_number):
        crud_utils.delete_from_stoplist(db, db_user.card_number)
    return new_balance
