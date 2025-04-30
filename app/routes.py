from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from services import crud_utils
from services.schemas.route import route_request, route_response
from services.crud_utils import get_bus_by_number, get_terminal_by_id
from db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


route_router = APIRouter(prefix='/route', tags=['Interaction with routes'])


@route_router.post(
    "/create/",
    response_model=route_response.ReturnId,
    description="Operation for creating route"
)
async def create_route(route: route_request.RouteCreate, db: Session = Depends(get_db)):
    company = await crud_utils.get_transport_company_by_name(db, tc_name=route.transport_company)
    if company is None:
        return route_response.ReturnId(msg=f"Transport company with name \'{route.transport_company}\' not found")
    bus = await get_bus_by_number(db, route.bus_number)
    if bus is None:
        return route_response.ReturnId(msg=f"Bus with number {route.bus_number} not found")
    terminal = await get_terminal_by_id(db, route.terminal_id)
    if terminal is None:
        return route_response.ReturnId(msg=f"Terminal with id={route.terminal_id} not found")
    return await route_response.ReturnId(id=crud_utils.create_route(db=db, route=route))


@route_router.put(
    "/update/",
    response_model=route_response.ReturnRoute,
    description="Operation for updating route by its id"
)
async def update_route_by_id(route_id: int, route: route_request.RouteUpdate, db: Session = Depends(get_db)):
    db_route = await crud_utils.get_route_by_id(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with id=\'{route_id}\' not found")
    return await crud_utils.update_route(db, route=route, route_id=route_id)


@route_router.delete(
    "/delete/",
    response_model=route_response.SuccessfulDeletion,
    description="Operation for deleting route by its id"
)
async def delete_route_by_id(route_id: int, db: Session = Depends(get_db)):
    db_route = await crud_utils.get_route_by_id(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with id=\'{route_id}\' not found")
    await crud_utils.delete_route(db, route_id=route_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }


@route_router.get(
    "/get-by-name/",
    response_model=route_response.ReturnRoute,
    description="Operation for getting route by its name"
)
async def read_route_by_route_name(route_name: str, db: Session = Depends(get_db)):
    db_route = await crud_utils.get_route_by_name(db, route_name=route_name)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with name=\'{route_name}\' not found")
    return db_route


@route_router.get(
    "/getlist-by-company-name/",
    response_model=list[route_response.ReturnRoute],
    description="Operation for getting routes by the name of the company that serves them"
)
async def read_routes_by_company_name(company_name: str, db: Session = Depends(get_db)):
    db_routes = await crud_utils.get_routes_by_company_name(db, company_name=company_name)
    if db_routes is None:
        raise HTTPException(status_code=404, detail=f"Route owned by the сompany with name=\'{company_name}\' not found")
    return db_routes


@route_router.get(
    "/get-list/",
    response_model=list[route_response.ReturnRoute],
    description="Operation for getting list of all routes"
)
async def read_routes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_routes = await crud_utils.get_routes(db, skip=skip, limit=limit)
    return db_routes
