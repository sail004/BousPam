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


owner_router = APIRouter(prefix='/carrier', tags=['Interaction with carriers'])


@owner_router.post("/create/") #, response_model=schemas.ProductCreate
async def create_transport_company_owner(owner: schemas.TCOwnerCreate, db: Session = Depends(get_db)):
    # db_owner_name = crud_utils.get_user_by_name(db, name=tc.owner_name)
    # if db_owner_name is None:
    #     raise HTTPException(status_code=404, detail=f"User with name=\'{tc.owner_name}\' not found")
    # db_owner_surname = crud_utils.get_user_by_surname(db, surname=tc.owner_surname)
    # if db_owner_surname is None:
    #     raise HTTPException(status_code=404, detail=f"User with surname=\'{tc.owner_surname}\' not found")
    return await crud_utils.create_transport_company_owner(db=db, owner=owner)


@owner_router.put("/update/") #, response_model=schemas.Product
async def update_transport_company_owner_by_id(owner_id: int, owner: schemas.TCOwnerUpdate, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    return await crud_utils.update_transport_company_owner(db, owner=owner, owner_id=owner_id)


@owner_router.get("/get-list/") #, response_model=List[schemas.Product]
async def read_transport_companies_owners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    owners = await crud_utils.get_transport_companies_owners(db, skip=skip, limit=limit)
    return owners


@owner_router.get("/get-by-id/") #, response_model=schemas.Product
async def read_transport_company_owner_by_id(owner_id: int, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    return db_tc_owner


@owner_router.get("/get-income/") #, response_model=schemas.Product
async def read_transport_company_income_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    income = await crud_utils.get_transport_company_income_by_id(db, tc_id=db_tc_owner.company_id)
    return income


@owner_router.get("/get-by-name/") #, response_model=schemas.Product
async def read_transport_company_owner_by_id(owner_name: str, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_name(db, owner_name=owner_name)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with name=\'{owner_name}\' not found")
    return db_tc_owner


@owner_router.put("/login/") #, response_model=List[schemas.Product]
async def login_transport_company_owner(auth_data: schemas.Login, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.login_transport_company_owner(db, login=auth_data.login, password=auth_data.password)
    if db_tc_owner == 'numb':
        return 'Incorrect login'
    if db_tc_owner == 'inc':
        return 'Incorrect password'
    return db_tc_owner


@owner_router.get("/get-company/") #, response_model=schemas.Product
async def read_transport_company_by_owner(owner_id: int, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    db_company = await crud_utils.get_transport_company_by_id(db, tc_id=db_tc_owner.company_id)
    return db_company


@owner_router.delete("/delete/") #, response_model=dict
async def delete_transport_company_owner_by_id(owner_id: int, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    await crud_utils.delete_transport_company_owner(db, owner_id=owner_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
