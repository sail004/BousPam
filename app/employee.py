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


employee_router = APIRouter(prefix='/employee', tags=['Взаимодействие с сотрудниками'])


@employee_router.post("/create/") #, response_model=schemas.ProductCreate
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    employee_exists = crud_utils.get_employee_by_phone_number(db, phone_number=employee.phone_number)
    login_exists = crud_utils.get_employee_by_login(db, login=employee.login)
    if login_exists:
        return 'The employee with this login has already been registered'
    if employee_exists:
        return 'The employee with this number has already been registered'
    return crud_utils.create_employee(db=db, employee=employee).id


@employee_router.get("/get-list/") #, response_model=List[schemas.Product]
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = crud_utils.get_employees(db, skip=skip, limit=limit)
    return employees


@employee_router.put("/login/") #, response_model=List[schemas.Product]
def login_employee(auth_data: schemas.Login, db: Session = Depends(get_db)):
    db_employee = crud_utils.login_employee(db, login=auth_data.login, password=auth_data.password)
    if db_employee == 'numb':
        return 'Incorrect login'
    if db_employee == 'inc':
        return 'Incorrect password'
    return db_employee


@employee_router.get("/get/") #, response_model=schemas.Product
def read_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud_utils.get_employee_by_id(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail=f"Employee with id=\'{employee_id}\' not found")
    return db_employee


@employee_router.put("/update/") #, response_model=schemas.Product
def update_employee_by_id(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = crud_utils.get_employee_by_id(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail=f"Employee with id=\'{employee_id}\' not found")
    return crud_utils.update_employee(db, employee=employee, employee_id=employee_id)


@employee_router.delete("/delete/") #, response_model=dict
def delete_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud_utils.get_employee_by_id(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail=f"Employee with id=\'{employee_id}\' not found")
    crud_utils.delete_employee(db, employee_id=employee_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }
