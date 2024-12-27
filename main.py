from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
import os
import crud_utils
import models
import schemas
from database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root = os.path.dirname(os.path.abspath(__file__))

#app.mount("/static", StaticFiles(directory="static"), name="static")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/registration/") #, response_model=schemas.ProductCreate
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    user_exists = crud_utils.get_user_by_phone_number(db, phone_number=user.phone_number)
    if user_exists:
        return 'The number has already been registered'
    return crud_utils.create_user(db=db, user=user).id


@app.get("/users/") #, response_model=List[schemas.Product]
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud_utils.get_users(db, skip=skip, limit=limit)
    return users


@app.get("/login/") #, response_model=List[schemas.Product]
def login_user(phone_number: str, password: str, db: Session = Depends(get_db)):
    db_user = crud_utils.login_user(db, phone_number=phone_number, password=password)
    if db_user == 'numb':
        return 'Incorrect phone number'
    if db_user == 'inc':
        return 'Incorrect password'
    return db_user


@app.get("/user/{user_id}") #, response_model=schemas.Product
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return db_user


@app.get("/balance/{user_id}") #, response_model=schemas.Product
def get_user_balance_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return crud_utils.get_balance_by_id(db, user_id=user_id)


@app.get("/operations/") #, response_model=List[schemas.Product]
def read_operations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    operations = crud_utils.get_operations(db, skip=skip, limit=limit)
    return operations


@app.get("/operations/{term_id}") #, response_model=schemas.Product
def read_operations_by_terminal_id(term_id: int, db: Session = Depends(get_db)):
    db_ops = crud_utils.get_operations_by_terminal_id(db, term_id=term_id)
    if db_ops is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{term_id}\' not found")
    return db_ops


@app.get("/operations_user/{user_id}") #, response_model=schemas.Product
def read_operations_by_user_id(user_id: int, db: Session = Depends(get_db)):
    db_ops = crud_utils.get_operations_by_user_id(db, user_id=user_id)
    if db_ops is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return db_ops


@app.put("/user/{user_id}") #, response_model=schemas.Product
def update_user_by_id(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return crud_utils.update_user(db, user=user, user_id=user_id)


@app.put("/payment/{user_id}") #, response_model=schemas.Product
def payment_by_user_id(operation: schemas.OperationPaymentCreate, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=operation.id_user)
    db_terminal = crud_utils.get_terminal_by_id(db, terminal_id=operation.id_terminal)
    if db_terminal is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{operation.id_terminal}\' not found")
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{operation.id_user}\' not found")
    delta_time = datetime.now() - operation.request_time
    #crud_utils.create_operation_payment(db, operation, 'payment')
    balance_change = crud_utils.create_operation_payment(db, operation, 'payment')
    if delta_time < timedelta(minutes=1):
        if db_user.balance < abs(balance_change):
            return HTTPException(status_code=400, detail=f"Insufficient funds to make the payment")
        else:
            crud_utils.create_operation_payment(db, operation, 'payment')
            return crud_utils.update_balance(db, user_id=operation.id_user, balance=-balance_change)
    return crud_utils.update_balance(db, user_id=operation.id_user, balance=-balance_change)


@app.put("/replenishment/{user_id}") #, response_model=schemas.Product
def replenishment_by_user_id(operation: schemas.OperationReplenishmentCreate, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=operation.id_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{operation.id_user}\' not found")
    crud_utils.create_operation_replenishment(db, operation, 'replenishment')
    return crud_utils.update_balance(db, user_id=operation.id_user, balance=operation.balance_change)


@app.delete("/user/{user_id}") #, response_model=dict
def delete_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    crud_utils.delete_user(db, user_id=user_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }


@app.post("/terminal/") #, response_model=schemas.ProductCreate
def create_terminal(terminal: schemas.TerminalCreate, db: Session = Depends(get_db)):
    db_route = crud_utils.get_route_by_name(db, route_name=terminal.route)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with name=\'{terminal.route}\' not found")
    return crud_utils.create_terminal(db=db, terminal=terminal).id


@app.get("/terminal/{term_id}") #, response_model=schemas.Product
def read_terminal_by_id(term_id: int, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminal_by_id(db, terminal_id=term_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{term_id}\' not found")
    return db_term


@app.get("/terminals/{company_name}") #, response_model=schemas.Product
def read_terminals_by_company_name(company_name: str, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminals_by_company(db, company_name=company_name)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Transport company with name=\'{company_name}\' not found")
    return db_term


@app.put("/terminal/{term_id}") #, response_model=schemas.Product
def update_terminal_by_id(term_id: int, term: schemas.TerminalUpdate, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminal_by_id(db, terminal_id=term_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{term_id}\' not found")
    return crud_utils.update_terminal(db, term=term, term_id=term_id)


@app.delete("/terminal/{term_id}") #, response_model=dict
def delete_terminal_by_id(term_id: int, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminal_by_id(db, terminal_id=term_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{term_id}\' not found")
    crud_utils.delete_terminal(db, terminal_id=term_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }


@app.post("/route/") #, response_model=schemas.ProductCreate
def create_route(route: schemas.RouteCreate, db: Session = Depends(get_db)):
    return crud_utils.create_route(db=db, route=route).id


@app.put("/route/{route_id}") #, response_model=schemas.Product
def update_route_by_id(route_id: int, route: schemas.RouteUpdate, db: Session = Depends(get_db)):
    db_route = crud_utils.get_route_by_id(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with id=\'{route_id}\' not found")
    return crud_utils.update_route(db, route=route, route_id=route_id)


@app.delete("/route/{route_id}") #, response_model=dict
def delete_route_by_id(route_id: int, db: Session = Depends(get_db)):
    db_route = crud_utils.get_route_by_id(db, route_id=route_id)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with id=\'{route_id}\' not found")
    crud_utils.delete_route(db, route_id=route_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }


@app.get("/route/{route_name}") #, response_model=schemas.Product
def read_route_by_route_name(route_name: str, db: Session = Depends(get_db)):
    db_route = crud_utils.get_route_by_name(db, route_name=route_name)
    if db_route is None:
        raise HTTPException(status_code=404, detail=f"Route with name=\'{route_name}\' not found")
    return db_route


@app.post("/tc/") #, response_model=schemas.ProductCreate
def create_transport_company(tc: schemas.TransportCompanyCreate, db: Session = Depends(get_db)):
    return crud_utils.create_transport_company(db=db, company=tc).id


@app.put("/tc/{tc_id}") #, response_model=schemas.Product
def update_transport_company_by_id(tc_id: int, tc: schemas.TransportCompanyUpdate, db: Session = Depends(get_db)):
    db_company = crud_utils.get_transport_company_by_id(db, tc_id=tc_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail=f"Company with id=\'{tc_id}\' not found")
    return crud_utils.update_transport_company(db, company=tc, tc_id=tc_id)


@app.delete("/tc/{tc_id}") #, response_model=dict
def delete_transport_company_by_id(tc_id: int, db: Session = Depends(get_db)):
    db_company = crud_utils.get_transport_company_by_id(db, tc_id=tc_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail=f"Company with id=\'{tc_id}\' not found")
    crud_utils.delete_transport_company(db, tc_id=tc_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }