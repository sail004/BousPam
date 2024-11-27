from datetime import datetime

from sqlalchemy.orm import Session
import models
import hashlib
import os
import schemas
from fastapi import HTTPException
# from . import models, schemas


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_balance_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first().balance

def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_user_by_phone_number(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).all()


def create_user(db: Session, user: schemas.UserCreate):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', user.password.encode('utf-8'), salt, 100000, dklen=128)
    db_user = models.User(
        name=user.name,
        surname=user.surname,
        balance=0.0,
        salt=salt,
        key=key,
        phone_number=user.phone_number,
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_operation_payment(db: Session, operation: schemas.OperationPaymentCreate, op_type: str):
    db_operation = models.Operation(
        type=op_type,
        id_terminal=operation.id_terminal,
        id_user=operation.id_user,
        balance_change=operation.balance_change,
        datetime=datetime.now())
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation


def create_operation_replenishment(db: Session, operation: schemas.OperationReplenishmentCreate, op_type: str):
    db_operation = models.Operation(
        type=op_type,
        bank_name=operation.bank_name,
        id_user=operation.id_user,
        balance_change=operation.balance_change,
        datetime=datetime.now())
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return db_operation


def update_user(db: Session, user: schemas.UserUpdate, user_id: int):
    db_user = get_user_by_id(db, user_id=user_id)
    user_data = user.dict()

    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    return db_user


def update_balance(db: Session, user_id: int, balance: float):
    db_user = get_user_by_id(db, user_id=user_id)
    balance += db_user.balance
    setattr(db_user, 'balance', balance)
    db.add(db_user)
    db.commit()
    return balance


def delete_user(db: Session, user_id: int):
    db_user = get_user_by_id(db, user_id=user_id)

    db.delete(db_user)
    db.commit()


def get_operations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Operation).all()


def get_operations_by_terminal_id(db: Session, term_id: int):
    return list(db.query(models.Operation).filter(models.Operation.id_terminal == term_id))


def get_operations_by_user_id(db: Session, user_id: int):
    return list(db.query(models.Operation).filter(models.Operation.id_user == user_id))


def create_terminal(db: Session, terminal: schemas.TerminalCreate):
    db_term = models.Terminal(
        transport_company=terminal.transport_company,
        route = terminal.route
    )
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term


def get_terminal_by_id(db: Session, terminal_id: int):
    return db.query(models.Terminal).filter(models.Terminal.id == terminal_id).first()


def update_terminal(db: Session, term: schemas.TerminalUpdate, term_id: int):
    db_term = get_terminal_by_id(db, terminal_id=term_id)
    term_data = term.dict()

    for key, value in term_data.items():
        setattr(db_term, key, value)
    db.add(db_term)
    db.commit()
    return db_term


def delete_terminal(db: Session, terminal_id: int):
    db_term = get_terminal_by_id(db, terminal_id=terminal_id)

    db.delete(db_term)
    db.commit()


def get_terminals_by_company(db: Session, company_name: str):
    return list(db.query(models.Terminal).filter(models.Terminal.transport_company == company_name))


def create_route(db: Session, route: schemas.RouteCreate):
    db_route = models.Route(
        transport_company=route.transport_company,
        name = route.name,
        stops = route.stops
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route


def get_route_by_id(db: Session, route_id: int):
    return db.query(models.Route).filter(models.Route.id == route_id).first()


def update_route(db: Session, route: schemas.RouteUpdate, route_id: int):
    db_route = get_route_by_id(db, route_id=route_id)
    route_data = route.dict()

    for key, value in route_data.items():
        setattr(db_route, key, value)
    db.add(db_route)
    db.commit()
    return db_route


def delete_route(db: Session, route_id: int):
    db_route = get_route_by_id(db, route_id=route_id)

    db.delete(db_route)
    db.commit()


def get_route_by_name(db: Session, route_name: str):
    return db.query(models.Route).filter(models.Route.name == route_name).first()


def login_user(db: Session, phone_number: str, password: str):
    user = db.query(models.User).filter(models.User.phone_number == phone_number).first()
    if user is None:
        return 'numb'
    salt = user.salt
    key = user.key
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000)
    if new_key == key:
        return user
    else:
        return False


def create_transport_company(db: Session, company: schemas.TransportCompanyCreate):
    db_company = models.TransportCompany(
        name=company.name,
        routes=company.routes,
        terminals=company.terminals
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


def get_transport_company_by_id(db: Session, tc_id: int) -> object:
    return db.query(models.TransportCompany).filter(models.TransportCompany.id == tc_id).first()


def update_transport_company(db: Session, company: schemas.TransportCompanyUpdate, tc_id: int):
    db_company = get_transport_company_by_id(db, tc_id=tc_id)
    company_data = company.dict()

    for key, value in company_data.items():
        setattr(db_company, key, value)
    db.add(db_company)
    db.commit()
    return db_company


def delete_transport_company(db: Session, tc_id: int):
    db_company = get_transport_company_by_id(db, tc_id=tc_id)

    db.delete(db_company)
    db.commit()
