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


route_router = APIRouter(prefix='/route', tags=['Interaction with routes'])


@route_router.post("/create/") #, response_model=schemas.ProductCreate
async def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    return await crud_utils.create_route(db=db, route=route)


@route_router.put("/update/") #, response_model=schemas.Product
async def update_route_by_id(route_id: int, route: schemas.RouteUpdate, db: Session = Depends(get_db)):
    db_route = await crud_utils.get_route_by_id(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with id=\'{route_id}\' not found")
    return await crud_utils.update_route(db, route=route, route_id=route_id)


@route_router.delete("/delete/") #, response_model=dict
async def delete_route_by_id(route_id: int, db: Session = Depends(get_db)):
    db_route = await crud_utils.get_route_by_id(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with id=\'{route_id}\' not found")
    await crud_utils.delete_route(db, route_id=route_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }


@route_router.get("/get-by-name/") #, response_model=schemas.Product
async def read_route_by_route_name(route_name: str, db: Session = Depends(get_db)):
    db_route = await crud_utils.get_route_by_name(db, route_name=route_name)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with name=\'{route_name}\' not found")
    return db_route
