from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils
from services.schemas.company import company_request, company_response
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


company_router = APIRouter(prefix='/company', tags=['Interaction with transport companies'])


@company_router.post(
    "/create/",
    response_model=company_response.ReturnId,
    description="Operation for creating transport company"
)
async def create_transport_company(tc: company_request.TransportCompanyCreate, db: Session = Depends(get_db)):
    # db_owner_name = crud_utils.get_user_by_name(db, name=tc.owner_name)
    # if db_owner_name is None:
    #     raise HTTPException(status_code=404, detail=f"User with name=\'{tc.owner_name}\' not found")
    # db_owner_surname = crud_utils.get_user_by_surname(db, surname=tc.owner_surname)
    # if db_owner_surname is None:
    #     raise HTTPException(status_code=404, detail=f"User with surname=\'{tc.owner_surname}\' not found")
    ans = await crud_utils.create_transport_company(db=db, company=tc)
    if type(ans) == str:
        return company_response.ReturnId(message=ans)
    return company_response.ReturnId(id=ans)


@company_router.put(
    "/update/",
    response_model=company_response.ReturnCompany,
    description="Operation for updating transport company by id"
)
async def update_transport_company_by_id(tc_id: int, tc: company_request.TransportCompanyUpdate, db: Session = Depends(get_db)):
    db_company = await crud_utils.get_transport_company_by_id(db, tc_id=tc_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail=f"Company with id=\'{tc_id}\' not found")
    return await crud_utils.update_transport_company(db, company=tc, tc_id=tc_id)


@company_router.get(
    "/get-list/",
    response_model=list[company_response.ReturnCompanyJoined],
    description="Operation for getting list of transport companies"
)
async def read_transport_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transport_companies = await crud_utils.get_transport_companies(db, skip=skip, limit=limit)
    tc_joined = []
    for company in transport_companies:
        tc = {
            "id": company.id,
            "name": company.name,
            "owner_number": company.owner_number,
            "owner": company.owner_name + ' ' + company.owner_surname,
        }
        tc_joined.append(tc)
    return tc_joined


@company_router.get("/get/",
    response_model=company_response.ReturnCompany,
    description="Operation for getting transport company by its name"
)
async def read_transport_company_by_name(company_name: str, db: Session = Depends(get_db)):
    db_company = await crud_utils.get_transport_company_by_name(db, tc_name=company_name)
    if db_company is None:
        raise HTTPException(status_code=404, detail=f"Company with name=\'{company_name}\' not found")
    return db_company


@company_router.delete("/delete/",
    response_model=company_response.SuccessfulDeletion,
    description="Operation for deleting transport company by its id"
)
async def delete_transport_company_by_id(tc_id: int, db: Session = Depends(get_db)):
    db_company = await crud_utils.get_transport_company_by_id(db, tc_id=tc_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail=f"Company with id=\'{tc_id}\' not found")
    await crud_utils.delete_transport_company(db, tc_id=tc_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
