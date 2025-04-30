from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils
from services.schemas.user import user_request, user_response
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


user_router = APIRouter(prefix='/passengers', tags=['Interaction with passengers'])


@user_router.post(
    "/registration/",
    response_model=user_response.ReturnId,
    description="Operation for registration passenger"
)
async def register_user(user: user_request.UserCreate, db: Session = Depends(get_db)):
    user_exists = await crud_utils.get_user_by_phone_number(db, phone_number=user.phone_number)
    if user_exists:
        return user_response.ReturnId(msg='The number has already been registered')
    return user_response.ReturnId(id=await crud_utils.create_user(db=db, user=user))


@user_router.get(
    "/getlist/",
    response_model=list[user_response.ReturnUser],
    description="Operation for getting list of all passengers"
)
async def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = await crud_utils.get_users(db, skip=skip, limit=limit)
    return users


@user_router.get(
    "/get-by-id/",
    response_model=user_response.ReturnUser,
    description="Operation for getting passenger by its id"
)
async def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return db_user


@user_router.get(
    "/get-balance/",
    response_model=user_response.ReturnBalance,
    description="Operation for getting passenger's balance by its id"
)
async def get_user_balance_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return user_response.ReturnBalance(balance=await crud_utils.get_balance_by_id(db, user_id=user_id))


@user_router.put(
    "/update-by-id/",
    response_model=user_response.ReturnUser,
    description="Operation for updating passenger by its id"
)
async def update_user_by_id(user_id: int, user: user_request.UserUpdate, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return await crud_utils.update_user(db, user=user, user_id=user_id)


@user_router.delete(
    "/user/{user_id}",
    response_model=user_response.SuccessfulDeletion,
    description="Operation for deleting passenger by its id"
)
async def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    await crud_utils.delete_user(db, user_id=user_id)
    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
