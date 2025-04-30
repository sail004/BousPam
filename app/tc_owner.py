from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils
from services.schemas.tc_owners import tc_owners_request, tc_owners_response
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


owner_router = APIRouter(prefix='/carrier', tags=['Interaction with carriers'])


@owner_router.post(
    "/create/",
    response_model=tc_owners_response.ReturnId,
    description="Operation for create transport company's owner"
)
async def create_transport_company_owner(owner: tc_owners_request.TCOwnerCreate, db: Session = Depends(get_db)):
    employee_exists = await crud_utils.get_transport_company_owner_by_phone_number(db, phone_number=owner.phone_number)
    login_exists = await crud_utils.get_transport_company_owner_by_login(db, login=owner.login)
    if login_exists:
        return tc_owners_response.ReturnId(msg='The TC owner with this login has already been registered')
    if employee_exists:
        return tc_owners_response.ReturnId(msg='The TC owner with this number has already been registered')
    return tc_owners_response.ReturnId(id=await crud_utils.create_transport_company_owner(db=db, owner=owner))


@owner_router.put(
    "/update/",
    response_model=tc_owners_response.ReturnTCOwner,
    description="Operation for updating info of transport company's owner"
)
async def update_transport_company_owner_by_id(owner_id: int, owner: tc_owners_request.TCOwnerUpdate, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    return await crud_utils.update_transport_company_owner(db, owner=owner, owner_id=owner_id)


@owner_router.get(
    "/get-list/",
    response_model=list[tc_owners_response.ReturnTCOwner],
    description="Operation for getting list of transport company's owners"
)
async def read_transport_companies_owners(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    owners = await crud_utils.get_transport_companies_owners(db, skip=skip, limit=limit)
    return owners


@owner_router.get(
    "/get-by-id/",
    response_model=tc_owners_response.ReturnTCOwner,
    description="Operation for getting transport company's owner info by its id"
)
async def read_transport_company_owner_by_id(owner_id: int, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    return db_tc_owner


@owner_router.get(
    "/get-income/",
    response_model=tc_owners_response.ReturnIncome,
    description="Operation for getting income of company by its owner's id"
)
async def read_transport_company_income_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    income = await crud_utils.get_transport_company_income_by_id(db, tc_id=db_tc_owner.company_id)
    return income


@owner_router.get(
    "/get-by-name/",
    response_model=tc_owners_response.ReturnTCOwner,
    description="Operation for getting transport company's owner info by its name"
)
async def read_transport_company_owner_by_name(owner_name: str, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_name(db, owner_name=owner_name)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with name=\'{owner_name}\' not found")
    return db_tc_owner


# @owner_router.put("/login/") #, response_model=List[schemas.Product]
# async def login_transport_company_owner(auth_data: schemas.Login, db: Session = Depends(get_db)):
#     db_tc_owner = await crud_utils.login_transport_company_owner(db, login=auth_data.login, password=auth_data.password)
#     if db_tc_owner == 'numb':
#         return 'Incorrect login'
#     if db_tc_owner == 'inc':
#         return 'Incorrect password'
#     return db_tc_owner


@owner_router.get(
    "/get-company/",
    response_model=tc_owners_response.ReturnCompanyInfo,
    description="Operation for getting transport company by its owner's id"
)
async def read_transport_company_by_owner(owner_id: int, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    db_company = await crud_utils.get_transport_company_by_id(db, tc_id=db_tc_owner.company_id)
    return db_company


@owner_router.delete(
    "/delete/",
    response_model=tc_owners_response.SuccessfulDeletion,
    description="Operation for deleting transport company owner by its id"
)
async def delete_transport_company_owner_by_id(owner_id: int, db: Session = Depends(get_db)):
    db_tc_owner = await crud_utils.get_transport_company_owner_by_id(db, owner_id=owner_id)
    if db_tc_owner is None:
        raise HTTPException(status_code=404, detail=f"Owner with id=\'{owner_id}\' not found")
    await crud_utils.delete_transport_company_owner(db, owner_id=owner_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
