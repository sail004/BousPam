from datetime import datetime, timedelta, timezone
from fastapi import Depends, FastAPI, HTTPException, APIRouter
from sqlalchemy.orm import Session
import os
import crud_utils
import models
import schemas
from database import SessionLocal, engine


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(prefix='/users', tags=['Работа с пользователями'])


@user_router.post("/registration/") #, response_model=schemas.ProductCreate
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = await crud_utils.get_user_by_phone_number(db, phone_number=user.phone_number)
    if user_exists:
        return 'The number has already been registered'
    return await crud_utils.create_user(db=db, user=user)


@user_router.get("/getlist/") #, response_model=List[schemas.Product]
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await crud_utils.get_users(db, skip=skip, limit=limit)
    return users


@user_router.get("/get-by-id/") #, response_model=schemas.Product
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return db_user


@user_router.get("/get-balance/") #, response_model=schemas.Product
async def get_user_balance_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return await crud_utils.get_balance_by_id(db, user_id=user_id)


@user_router.put("/update-by-id/") #, response_model=schemas.Product
async def update_user_by_id(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return await crud_utils.update_user(db, user=user, user_id=user_id)


@user_router.delete("/user/{user_id}") #, response_model=dict
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    await crud_utils.delete_user(db, user_id=user_id)
    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
