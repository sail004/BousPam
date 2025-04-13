from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils, schemas
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


login_router = APIRouter(prefix='/login', tags=['Login'])


@login_router.put("/") #, response_model=List[schemas.Product]
async def login(auth_data: schemas.Login, db: Session = Depends(get_db)):
    db_employee = await crud_utils.login_employee(db, login=auth_data.login, password=auth_data.password)
    db_tc_owner = await crud_utils.login_transport_company_owner(db, login=auth_data.login, password=auth_data.password)
    if db_employee == 'numb' and db_tc_owner == 'numb':
        return 'Incorrect login'
    if db_employee == 'inc' or db_tc_owner == 'inc':
        return 'Incorrect password'
    return db_employee if type(db_employee) != str else db_tc_owner