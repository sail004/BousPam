from fastapi import Depends, HTTPException, APIRouter, status
from sqlalchemy.orm import Session
from services import crud_utils
from services.schemas.bus import bus_request, bus_response
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


bus_router = APIRouter(prefix='/buses', tags=['Interaction with buses'])


@bus_router.post(
    "/create/",
    response_model=bus_response.ReturnId,
    description="Operation for creating buses"
)
async def create_bus(bus: bus_request.BusCreate, db: Session = Depends(get_db)):
    return bus_response.ReturnId(id=await crud_utils.create_bus(db=db, bus=bus))


@bus_router.put(
    "/update/",
    response_model=bus_response.ReturnBus,
    description="Operation for updating buses"
)
async def update_bus_by_id(bus_id: int, bus: bus_request.BusUpdate, db: Session = Depends(get_db)):
    db_bus = await crud_utils.get_bus_by_id(db, bus_id=bus_id)
    if db_bus is None:
        raise HTTPException(status_code=404, detail=f"Bus with id=\'{bus_id}\' not found")
    return await crud_utils.update_bus(db, bus=bus, bus_id=bus_id)


@bus_router.get(
    "/get-by-number/",
    response_model=bus_response.ReturnBus,
    description="Operation for getting bus by its number"
)
async def read_bus_by_number(bus_number: str, db: Session = Depends(get_db)):
    db_bus = await crud_utils.get_bus_by_number(db, bus_number=bus_number)
    if db_bus is None:
        raise HTTPException(status_code=404, detail=f"Bus with number=\'{bus_number}\' not found")
    return db_bus


@bus_router.get(
    "/get-by-company-name/",
    response_model=list[bus_response.ReturnBus],
    description="Operation for getting buses by name of company that owns that buses"
)
async def read_buses_by_company_name(company_name: str, db: Session = Depends(get_db)):
    db_buses = await crud_utils.get_buses_by_company_name(db, company_name=company_name)
    if db_buses is None:
        raise HTTPException(status_code=404, detail=f"Buses owned by the сompany with name=\'{company_name}\' not found")
    return db_buses


@bus_router.get(
    "/get-list/",
    response_model=list[bus_response.ReturnBus],
    description="Operation for getting all buses with skip and limit"
)
async def read_buses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    buses = await crud_utils.get_buses(db, skip=skip, limit=limit)
    return buses


@bus_router.delete(
    "/delete/",
    response_model=bus_response.SuccessfulDeletion,
    description="Operation for deleting bus by its id"
)
async def delete_bus_by_id(bus_id: int, db: Session = Depends(get_db)):
    db_bus = await crud_utils.get_bus_by_id(db, bus_id=bus_id)
    if db_bus is None:
        raise HTTPException(status_code=404, detail=f"Bus with id=\'{bus_id}\' not found")
    await crud_utils.delete_bus(db, bus_id=bus_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
