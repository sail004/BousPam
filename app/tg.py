from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils, schemas
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


tg_router = APIRouter(prefix='/tg', tags=['Interaction with telegram mini app'])


@tg_router.get("/read-user/tg-id/") #, response_model=schemas.Product
async def read_user_by_tg_id(tg_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_tg_id(db, tg_id=tg_id)
    if db_user is None:
        return {}
        #raise HTTPException(status_code=404, detail=f"User with tg_id=\'{tg_id}\' not found")
    info = await crud_utils.get_all_info_by_tg_id(db, tg_id=tg_id)
    return info


@tg_router.post("/read-user/card-number/") #, response_model=schemas.Product
async def read_user_by_card_number(card: schemas.TgCard, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_card_number(db, card_number=card.number)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with card_number=\'{card.number}\' not found")
    return db_user


@tg_router.put("/employee/set-tg-id/") #, response_model=schemas.Product
async def set_employee_tg_id(tg: schemas.SetTgId, db: Session = Depends(get_db)):
    db_employee = await crud_utils.get_employee_by_id(db, employee_id=tg.entity_id)
    if db_employee is None:
        return f"Employee with id=\'{tg.entity_id}\' not found"
    return await crud_utils.set_employee_tg_id(db, info=tg)


@tg_router.put("/carrier/set-tg-id/") #, response_model=schemas.Product
async def set_owner_tg_id(tg: schemas.SetTgId, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=tg.entity_id)
    if db_tc_owner is None:
        return f"Transport company's owner with id=\'{tg.entity_id}\' not found"
    return await crud_utils.set_transport_company_owner_tg_id(db, info=tg)


@tg_router.put("/user/set-tg-id/") #, response_model=schemas.Product
async def set_user_tg_id_for_user(card: schemas.TgCard, tg_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_card_number(db, card_number=card.number)
    if db_user is None:
        return f"User with card_number=\'{card.number}\' not found"
    return await crud_utils.set_user_tg_id(db, tg_id=tg_id, card_number=card.number)


@tg_router.get("/user/operations/") #, response_model=schemas.Product
async def read_operations_by_tg_id(tg_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_tg_id(db, tg_id=tg_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with tg_id={tg_id} not found")
    db_ops = await crud_utils.get_operations_by_user_id(db, user_id=db_user.id)
    if db_ops is None:
        raise HTTPException(status_code=404, detail=f"Operations not found")
    return db_ops


@tg_router.get("/user/balance/") #, response_model=schemas.Product
async def get_user_balance_by_tg_id(tg_id: int, db: Session = Depends(get_db)):
    db_user = await crud_utils.get_user_by_tg_id(db, tg_id=tg_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with tg_id=\'{tg_id}\' not found")
    return await crud_utils.get_balance_by_id(db, user_id=db_user.id)
