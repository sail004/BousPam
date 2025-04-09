from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random
import string
import random
import models
import hashlib
import os
import schemas
import services.luhn
from services.luhn import set_luhn


async def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_balance_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first().balance


def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


def get_user_by_surname(db: Session, surname: str):
    return db.query(models.User).filter(models.User.surname == surname).first()


async def get_user_by_phone_number(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()


async def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


async def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        surname=user.surname,
        balance=0.0,
        phone_number=user.phone_number,
        card_number=user.card_number,
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id


async def get_price_by_terminal_id(db: Session, terminal_id: int):
    terminal = await get_terminal_by_id(db=db, terminal_id=terminal_id)
    return terminal.fare


async def create_operation_payment(db: Session, operation: schemas.OperationPaymentCreate, op_type: str):
    price = await get_price_by_terminal_id(db=db, terminal_id=operation.id_terminal)
    db_operation = models.Operation(
        type=op_type,
        id_terminal=operation.id_terminal,
        id_user=operation.id_user,
        balance_change=-price,
        datetime=operation.request_time,
        terminal_hash=operation.terminal_hash
    )
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return await update_balance(db, operation.id_user, -price)


async def create_operation_replenishment(db: Session, operation: schemas.OperationReplenishmentCreate, op_type: str):
    db_operation = models.Operation(
        type=op_type,
        id_user=operation.id_user,
        balance_change=operation.balance_change,
        datetime=datetime.now())
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return await update_balance(db, operation.id_user, operation.balance_change)


async def update_user(db: Session, user: schemas.UserUpdate, user_id: int):
    db_user = await get_user_by_id(db, user_id=user_id)
    user_data = user.dict()

    for key, value in user_data.items():
        setattr(db_user, key, value)
    db.add(db_user)
    db.commit()
    return db_user


async def update_balance(db: Session, user_id: int, balance: float):
    db_user = await get_user_by_id(db, user_id=user_id)
    balance += db_user.balance
    setattr(db_user, 'balance', balance)
    db.add(db_user)
    db.commit()
    return balance


async def delete_user(db: Session, user_id: int):
    db_user = await get_user_by_id(db, user_id=user_id)

    db.delete(db_user)
    db.commit()


async def get_operations(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Operation).offset(skip).limit(limit).all()


async def get_operations_by_terminal_id(db: Session, term_id: int):
    return list(db.query(models.Operation).filter(models.Operation.id_terminal == term_id))


async def get_operations_by_user_id(db: Session, user_id: int):
    return list(db.query(models.Operation).filter(models.Operation.id_user == user_id))


async def create_terminal(db: Session, terminal: schemas.TerminalCreate):
    random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
    hash = hashlib.pbkdf2_hmac('sha256', random_string.encode('utf-8'), os.urandom(32), 100000, dklen=128)
    db_term = models.Terminal(
        company=terminal.company_name,
        fare=terminal.fare,
        hash=hash.hex()
    )
    db.add(db_term)
    db.commit()
    db.refresh(db_term)
    return db_term


async def get_terminal_by_id(db: Session, terminal_id: int):
    return db.query(models.Terminal).filter(models.Terminal.terminal_id == terminal_id).first()


async def update_terminal(db: Session, term: schemas.TerminalUpdate, term_id: int):
    db_term = await get_terminal_by_id(db, terminal_id=term_id)
    term_data = term.dict()

    for key, value in term_data.items():
        setattr(db_term, key, value)
    db.add(db_term)
    db.commit()
    return db_term


async def delete_terminal(db: Session, terminal_id: int):
    db_term = await get_terminal_by_id(db, terminal_id=terminal_id)

    db.delete(db_term)
    db.commit()


async def get_terminals_by_company(db: Session, company_name: str):
    return list(db.query(models.Terminal).filter(models.Terminal.company == company_name))


def login_user(db: Session, phone_number: str, password: str):
    user = db.query(models.User).filter(models.User.phone_number == phone_number).first()
    if user is None:
        return 'numb'
    salt = bytes.fromhex(user.salt)
    key = bytes.fromhex(user.key)
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,
        dklen=128)
    if new_key == key:
        return user
    return 'inc'


async def create_transport_company(db: Session, company: schemas.TransportCompanyCreate):
    db_company = models.TransportCompany(
        name=company.name,
        owner_name=company.owner_name,
        owner_surname=company.owner_surname
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company.id


async def get_transport_company_by_id(db: Session, tc_id: int) -> object:
    return db.query(models.TransportCompany).filter(models.TransportCompany.id == tc_id).first()


async def get_transport_company_by_name(db: Session, tc_name: str) -> object:
    return db.query(models.TransportCompany).filter(models.TransportCompany.name == tc_name).first()


async def update_transport_company(db: Session, company: schemas.TransportCompanyUpdate, tc_id: int):
    db_company = await get_transport_company_by_id(db, tc_id=tc_id)
    company_data = company.dict()

    for key, value in company_data.items():
        setattr(db_company, key, value)
    db.add(db_company)
    db.commit()
    return db_company


async def delete_transport_company(db: Session, tc_id: int):
    db_company = await get_transport_company_by_id(db, tc_id=tc_id)

    db.delete(db_company)
    db.commit()


async def get_transport_companies(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TransportCompany).offset(skip).limit(limit).all()


def get_terminals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Terminal).offset(skip).limit(limit).all()


def create_employee(db: Session, employee: schemas.EmployeeCreate):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', employee.password.encode('utf-8'), salt, 100000, dklen=128)
    db_employee = models.Employee(
        name=employee.name,
        surname=employee.surname,
        login=employee.login,
        gender=employee.gender,
        date_of_birth=employee.date_of_birth,
        salt=salt.hex(),
        key=key.hex(),
        role=employee.role,
        phone_number=employee.phone_number,
        )
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee


async def get_employee_by_phone_number(db: Session, phone_number: str):
    return db.query(models.Employee).filter(models.Employee.phone_number == phone_number).first()


async def get_employee_by_login(db: Session, login: str):
    return db.query(models.Employee).filter(models.Employee.login == login).first()


def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


def login_employee(db: Session, login: str, password: str):
    employee = db.query(models.Employee).filter(models.Employee.login == login).first()
    if employee is None:
        return 'numb'
    salt = bytes.fromhex(employee.salt)
    key = bytes.fromhex(employee.key)
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,
        dklen=128)
    if new_key == key:
        return employee
    return 'inc'


def get_employee_by_id(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


def update_employee(db: Session, employee: schemas.EmployeeUpdate, employee_id: int):
    db_employee = get_employee_by_id(db, employee_id=employee_id)
    employee_data = employee.dict()

    for key, value in employee_data.items():
        setattr(db_employee, key, value)
    db.add(db_employee)
    db.commit()
    return db_employee


def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee_by_id(db, employee_id=employee_id)

    db.delete(db_employee)
    db.commit()


def get_user_by_tg_id(db: Session, tg_id: int):
    return db.query(models.User).filter(models.User.tg_id == tg_id).first()


def get_user_by_card_number(db: Session, card_number: str):
    return db.query(models.User).filter(models.User.card_number == card_number).first()


def set_user_tg_id(db: Session, tg_id: int, card_number: str):
    db_user = get_user_by_card_number(db, card_number=card_number)
    setattr(db_user, 'tg_id', tg_id)
    db.add(db_user)
    db.commit()
    return 'success'


def get_all_info_by_tg_id(db: Session, tg_id: int):
    db_user = get_user_by_tg_id(db, tg_id=tg_id)
    operations = get_operations_by_user_id(db, user_id=db_user.id)
    card_number = db_user.card_number
    balance = db_user.balance
    re_object = {
        "card_number": card_number,
        "balance": balance,
        "operations": operations
    }
    return re_object


async def add_to_stoplist(db: Session, stoplist: schemas.StopListCreate):
    db_card = models.StopList(
        card_number=stoplist.card_number,
        owner_id=stoplist.owner_id,
        owner_phone_number=stoplist.owner_phone_number
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


async def get_card_from_stoplist(db: Session, card_number: str):
    return db.query(models.StopList).filter(models.StopList.card_number == card_number).first()


async def is_in_stoplist(db: Session, card_number: str):
    user = await get_card_from_stoplist(db, card_number=card_number)
    if user is None:
        return False
    return True


async def delete_from_stoplist(db: Session, card_number: str):
    db_card = await get_card_from_stoplist(db, card_number=card_number)
    db.delete(db_card)
    db.commit()


async def get_stoplist(db: Session):
    return db.query(models.StopList).all()


def get_next_card_number(db: Session):
    last_card = db.query(models.LastCardNumber).first()
    card_number = last_card.card_number
    new_card_number = str(int(card_number) + 1)
    len_new = len(new_card_number)
    if len_new < 9:
        new_card_number = (9 - len_new) * ' ' + new_card_number
    setattr(last_card, 'card_number', new_card_number)
    db.add(last_card)
    db.commit()
    return set_luhn(new_card_number)


def create_card(db: Session, card: schemas.CardCreate):
    db_card = models.Card(
        card_number=get_next_card_number(db),
        owner_id=card.owner_id,
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    return db_card


def get_cards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Card).offset(skip).limit(limit).all()


def get_card_by_id(db: Session, card_id: int):
    return db.query(models.Card).filter(models.Card.id == card_id).first()


def update_card(db: Session, card: schemas.CardUpdate, card_id: int):
    db_card = get_card_by_id(db, card_id=card_id)
    card_data = card.dict()

    for key, value in card_data.items():
        setattr(db_card, key, value)
    db.add(db_card)
    db.commit()
    return db_card


def delete_card(db: Session, card_id: int):
    db_card = get_card_by_id(db, card_id=card_id)

    db.delete(db_card)
    db.commit()
