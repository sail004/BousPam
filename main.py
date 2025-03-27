from datetime import datetime, timedelta, timezone


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


#@app.get("/login/") #, response_model=List[schemas.Product]
#def login_user(phone_number: str, password: str, db: Session = Depends(get_db)):
#    db_user = crud_utils.login_user(db, phone_number=phone_number, password=password)
#    if db_user == 'numb':
#        return 'Incorrect phone number'
#    if db_user == 'inc':
#        return 'Incorrect password'
#    return db_user


@app.get("/user/{user_id}") #, response_model=schemas.Product
def read_user_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return db_user


@app.get("/tg/users/{user_tg_id}") #, response_model=schemas.Product
def read_user_by_tg_id(tg_id: int, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_tg_id(db, tg_id=tg_id)
    if db_user is None:
        return {}
        #raise HTTPException(status_code=404, detail=f"User with tg_id=\'{tg_id}\' not found")
    info = crud_utils.get_all_info_by_tg_id(db, tg_id=tg_id)
    return info


@app.get("/tg/user/{card_number}") #, response_model=schemas.Product
def read_user_by_card_number(card_number: str, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_card_number(db, card_number=card_number)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with card_number=\'{card_number}\' not found")
    return db_user


@app.put("/tg/user/{card_number}") #, response_model=schemas.Product
def set_user_tg_id(card_number: str, tg_id: int, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_card_number(db, card_number=card_number)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with card_number=\'{card_number}\' not found")
    return crud_utils.set_user_tg_id(db, tg_id=tg_id, card_number=card_number)


@app.get("/tg/operations_user/{tg_id}") #, response_model=schemas.Product
def read_operations_by_tg_id(tg_id: int, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_tg_id(db, tg_id=tg_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with tg_id={tg_id} not found")
    db_ops = crud_utils.get_operations_by_user_id(db, user_id=db_user.id)
    if db_ops is None:
        raise HTTPException(status_code=404, detail=f"Operations not found")
    return db_ops


@app.get("/balance/{user_id}") #, response_model=schemas.Product
def get_user_balance_by_id(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{user_id}\' not found")
    return crud_utils.get_balance_by_id(db, user_id=user_id)


@app.get("/tg/balance/{tg_id}") #, response_model=schemas.Product
def get_user_balance_by_tg_id(tg_id: int, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_tg_id(db, tg_id=tg_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with tg_id=\'{tg_id}\' not found")
    return crud_utils.get_balance_by_id(db, user_id=db_user.id)


@app.get("/operations/") #, response_model=List[schemas.Product]
def read_operations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    operations = crud_utils.get_operations(db, skip=skip, limit=limit)
    return operations


@app.get("/operations/{term_id}") #, response_model=schemas.Product
def read_operations_by_terminal_id(terminal_id: int, db: Session = Depends(get_db)):
    db_ops = crud_utils.get_operations_by_terminal_id(db, term_id=terminal_id)
    if db_ops is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
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
    if db_terminal.hash != operation.terminal_hash:
        raise HTTPException(status_code=404, detail=f"Incorrect terminal hash")
    delta_time = datetime.now() - operation.request_time.replace(tzinfo=None)
    #crud_utils.create_operation_payment(db, operation, 'payment')
    balance_change = crud_utils.get_price_by_terminal_id(db, operation.id_terminal)
    if delta_time < timedelta(minutes=1):
        if db_user.balance < abs(balance_change):
            raise HTTPException(status_code=400, detail=f"Insufficient funds to make the payment")
        else:
            return crud_utils.create_operation_payment(db, operation, 'payment')
    return crud_utils.create_operation_payment(db, operation, 'payment')


@app.put("/replenishment/{user_id}") #, response_model=schemas.Product
def replenishment_by_user_id(operation: schemas.OperationReplenishmentCreate, db: Session = Depends(get_db)):
    db_user = crud_utils.get_user_by_id(db, user_id=operation.id_user)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f"User with id=\'{operation.id_user}\' not found")
    return crud_utils.create_operation_replenishment(db, operation, 'replenishment')


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
    db_tc = crud_utils.get_transport_company_by_name(db, tc_name=terminal.company_name)
    if db_tc is None:
        raise HTTPException(status_code=404, detail=f"Transport company with name=\'{terminal.company_name}\' not found")
    return crud_utils.create_terminal(db=db, terminal=terminal)


@app.get("/terminal/{term_id}") #, response_model=schemas.Product
def read_terminal_by_id(terminal_id: int, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminal_by_id(db, terminal_id=terminal_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    return db_term


@app.get("/terminals/") #, response_model=List[schemas.Product]
def read_terminals(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    terminals = crud_utils.get_terminals(db, skip=skip, limit=limit)
    return terminals


@app.get("/terminals/{company_name}") #, response_model=schemas.Product
def read_terminals_by_company_name(company_name: str, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminals_by_company(db, company_name=company_name)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Transport company with name=\'{company_name}\' not found")
    return db_term


@app.put("/terminal/{term_id}") #, response_model=schemas.Product
def update_terminal_by_id(terminal_id: int, term: schemas.TerminalUpdate, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminal_by_id(db, terminal_id=terminal_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    return crud_utils.update_terminal(db, term=term, term_id=terminal_id)


@app.delete("/terminal/{term_id}") #, response_model=dict
def delete_terminal_by_id(terminal_id: int, db: Session = Depends(get_db)):
    db_term = crud_utils.get_terminal_by_id(db, terminal_id=terminal_id)
    if db_term is None:
        raise HTTPException(status_code=404, detail=f"Terminal with id=\'{terminal_id}\' not found")
    crud_utils.delete_terminal(db, terminal_id=terminal_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }


@app.post("/tc/") #, response_model=schemas.ProductCreate
def create_transport_company(tc: schemas.TransportCompanyCreate, db: Session = Depends(get_db)):
    # db_owner_name = crud_utils.get_user_by_name(db, name=tc.owner_name)
    # if db_owner_name is None:
    #     raise HTTPException(status_code=404, detail=f"User with name=\'{tc.owner_name}\' not found")
    # db_owner_surname = crud_utils.get_user_by_surname(db, surname=tc.owner_surname)
    # if db_owner_surname is None:
    #     raise HTTPException(status_code=404, detail=f"User with surname=\'{tc.owner_surname}\' not found")
    return crud_utils.create_transport_company(db=db, company=tc).id


@app.put("/tc/{tc_id}") #, response_model=schemas.Product
def update_transport_company_by_id(tc_id: int, tc: schemas.TransportCompanyUpdate, db: Session = Depends(get_db)):
    db_company = crud_utils.get_transport_company_by_id(db, tc_id=tc_id)
    if db_company is None:
        raise HTTPException(status_code=404, detail=f"Company with id=\'{tc_id}\' not found")
    return crud_utils.update_transport_company(db, company=tc, tc_id=tc_id)


@app.get("/tcs/") #, response_model=List[schemas.Product]
def read_transport_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    transport_companies = crud_utils.get_transport_companies(db, skip=skip, limit=limit)
    tc_joined = []
    for company in transport_companies:
        tc = {
            "id": company.id,
            "name": company.name,
            "owner": company.owner_name + ' ' + company.owner_surname,
        }
        tc_joined.append(tc)
    return tc_joined


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


@app.post("/employee/") #, response_model=schemas.ProductCreate
def create_employee(employee: schemas.EmployeeCreate, db: Session = Depends(get_db)):
    employee_exists = crud_utils.get_employee_by_phone_number(db, phone_number=employee.phone_number)
    login_exists = crud_utils.get_employee_by_login(db, login=employee.login)
    if login_exists:
        return 'The employee with this login has already been registered'
    if employee_exists:
        return 'The employee with this number has already been registered'
    return crud_utils.create_employee(db=db, employee=employee).id


@app.get("/employees/") #, response_model=List[schemas.Product]
def read_employees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    employees = crud_utils.get_employees(db, skip=skip, limit=limit)
    return employees


@app.get("/loginemployee/") #, response_model=List[schemas.Product]
def login_employee(login: str, password: str, db: Session = Depends(get_db)):
    db_employee = crud_utils.login_employee(db, login=login, password=password)
    if db_employee == 'numb':
        return 'Incorrect login'
    if db_employee == 'inc':
        return 'Incorrect password'
    return db_employee


@app.get("/employee/{employee_id}") #, response_model=schemas.Product
def read_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud_utils.get_employee_by_id(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail=f"Employee with id=\'{employee_id}\' not found")
    return db_employee


@app.put("/employee/{employee_id}") #, response_model=schemas.Product
def update_employee_by_id(employee_id: int, employee: schemas.EmployeeUpdate, db: Session = Depends(get_db)):
    db_employee = crud_utils.get_employee_by_id(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail=f"Employee with id=\'{employee_id}\' not found")
    return crud_utils.update_employee(db, employee=employee, employee_id=employee_id)


@app.delete("/employee/{employee_id}") #, response_model=dict
def delete_employee_by_id(employee_id: int, db: Session = Depends(get_db)):
    db_employee = crud_utils.get_employee_by_id(db, employee_id=employee_id)
    if db_employee is None:
        raise HTTPException(status_code=404, detail=f"Employee with id=\'{employee_id}\' not found")
    crud_utils.delete_employee(db, employee_id=employee_id)

    return {
        "status": "ok",
        "message": "Deletion was successful"
    }


@app.get("/tc/{tc_name}") #, response_model=schemas.Product
def read_transport_company_by_name(company_name: str, db: Session = Depends(get_db)):
    db_company = crud_utils.get_transport_company_by_name(db, tc_name=company_name)
    if db_company is None:
        raise HTTPException(status_code=404, detail=f"Company with name=\'{company_name}\' not found")
    return db_company
