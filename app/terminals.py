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


terminal_router = APIRouter(prefix='/terminals', tags=['Взаимодействие с терминалами'])


@terminal_router.post("/create/") #, response_model=schemas.ProductCreate
def create_terminal(terminal: schemas.TerminalCreate, db: Session = Depends(get_db)):
    db_tc = crud_utils.get_transport_company_by_name(db, tc_name=terminal.company_name)
    if db_tc is None:
        raise HTTPException(status_code=404, detail=f"Transport company with name=\'{terminal.company_name}\' not found")
    return crud_utils.create_terminal(db=db, terminal=terminal)


@terminal_router.get("/get/by-id/") #, response_model=schemas.Product
def read_terminal_by_id(terminal_id: int, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminal_by_id(db, terminal_id=terminal_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    return db_term


@terminal_router.get("/get-list/") #, response_model=List[schemas.Product]
def read_terminals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terminals = crud_utils.get_terminals(db, skip=skip, limit=limit)
    return terminals


@terminal_router.get("/get/by-company/") #, response_model=schemas.Product
def read_terminals_by_company_name(company_name: str, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminals_by_company(db, company_name=company_name)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Transport company with name=\'{company_name}\' not found")
    return db_term


@terminal_router.put("/update/") #, response_model=schemas.Product
def update_terminal_by_id(terminal_id: int, term: schemas.TerminalUpdate, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminal_by_id(db, terminal_id=terminal_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    return crud_utils.update_terminal(db, term=term, term_id=terminal_id)


@terminal_router.delete("/delete/") #, response_model=dict
def delete_terminal_by_id(terminal_id: int, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminal_by_id(db, terminal_id=terminal_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    crud_utils.delete_terminal(db, terminal_id=terminal_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }

@terminal_router.get("/get-stoplist/") #, response_model=List[schemas.Product]
def read_stoplist(db: Session = Depends(get_db)):
    stoplist = crud_utils.get_stoplist(db)
    return stoplist
