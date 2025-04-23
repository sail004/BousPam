from datetime import datetime
import requests
from sqlalchemy.orm import Session
from sqlalchemy.sql.functions import random
from sqlalchemy.orm.attributes import flag_modified
import string
import random
from db import models
import hashlib
import os
from services.schemas import schemas
from services.luhn import set_luhn


LAGO_URL="http://localhost:3000"
API_KEY="d9ac4289-124c-4108-8327-13df555f96de"


async def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


async def get_balance_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first().balance


async def get_user_by_name(db: Session, name: str):
    return db.query(models.User).filter(models.User.name == name).first()


async def get_user_by_surname(db: Session, surname: str):
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
        e_mail=user.e_mail,
        niu=user.niu,
        nif=user.nif,
        passport_number=user.passport_number,
        phone_number=user.phone_number,
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user.id


async def get_price_by_terminal_id(db: Session, terminal_id: int):
    terminal = await get_terminal_by_id(db=db, terminal_id=terminal_id)
    return terminal.fare


async def payment_by_billing(id_user: int, id_terminal: int, fee: float):
    url = LAGO_URL + "/api/v1/invoices"  # /api/v1
    headers = {"Authorization": "Bearer " + API_KEY, 'Content-Type': 'application/json'}
    data = {"invoice": {
      "external_customer_id": str(id_user),
      "currency": "HTG",
      "fees": [
        {
          "add_on_code": "1",
          "units": 1,
          "unit_amount_cents": fee * 100,
          "description": str(id_terminal)
        },
        ]
    }
    }
    requests.post(url=url, headers=headers, json=data)


async def create_operation_payment(db: Session, operation: schemas.OperationPaymentCreate, op_type: str, user_id: int):
    price = await get_price_by_terminal_id(db=db, terminal_id=operation.id_terminal)
    db_operation = models.Operation(
        type=op_type,
        id_user=user_id,
        balance_change=operation.balance_change,
        datetime=datetime.now(),
        id_terminal=operation.id_terminal,
        terminal_hash=operation.terminal_hash,
        cashbox_number=operation.cashbox_number,
    )
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    #await payment_by_billing(user_id, operation.id_terminal, price)
    return await update_balance(db, user_id, -price)


async def create_operation_replenishment(db: Session, operation: schemas.OperationReplenishmentCreate, op_type: str, user_id: int):
    db_operation = models.Operation(
        type=op_type,
        id_user=user_id,
        balance_change=operation.balance_change,
        datetime=datetime.now(),
        cashier_id=operation.cashier_id,
        cashbox_number=operation.cashbox_number,
    )
    db.add(db_operation)
    db.commit()
    db.refresh(db_operation)
    return await update_balance(db, user_id, operation.balance_change)


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


async def login_user(db: Session, phone_number: str, password: str):
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
    db_owner = await get_transport_company_owner_by_id(db, owner_id=company.owner_id)
    if not db_owner:
        return f'Owner with id=\'{company.owner_id}\' does not exist'
    db_company = models.TransportCompany(
        name=company.name,
        owner_name=db_owner.name,
        owner_surname=db_owner.surname,
        owner_number=db_owner.phone_number,
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    id = db_company.id
    setattr(db_owner, 'company_id', db_company.id)
    db.add(db_owner)
    db.commit()
    return id


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


async def get_terminals(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Terminal).offset(skip).limit(limit).all()


async def create_employee(db: Session, employee: schemas.EmployeeCreate):
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
    return db_employee.id


async def get_employee_by_phone_number(db: Session, phone_number: str):
    return db.query(models.Employee).filter(models.Employee.phone_number == phone_number).first()


async def get_employee_by_login(db: Session, login: str):
    return db.query(models.Employee).filter(models.Employee.login == login).first()


async def get_employees(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Employee).offset(skip).limit(limit).all()


async def login_employee(db: Session, login: str, password: str):
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


async def get_employee_by_id(db: Session, employee_id: int):
    return db.query(models.Employee).filter(models.Employee.id == employee_id).first()


async def update_employee(db: Session, employee: schemas.EmployeeUpdate, employee_id: int):
    db_employee = await get_employee_by_id(db, employee_id=employee_id)
    employee_data = employee.dict()

    for key, value in employee_data.items():
        setattr(db_employee, key, value)
    db.add(db_employee)
    db.commit()
    return db_employee


async def delete_employee(db: Session, employee_id: int):
    db_employee = get_employee_by_id(db, employee_id=employee_id)

    db.delete(db_employee)
    db.commit()


async def get_user_by_tg_id(db: Session, tg_id: int):
    return db.query(models.User).filter(models.User.tg_id == tg_id).first()


async def get_user_by_card_number(db: Session, card_number: str):
    return db.query(models.User).filter(models.User.cards.contains([card_number])).first()


async def set_user_tg_id(db: Session, tg_id: int, card_number: str):
    db_user = await get_user_by_card_number(db, card_number=card_number)
    setattr(db_user, 'tg_id', tg_id)
    db.add(db_user)
    db.commit()
    return 'success'


async def set_employee_tg_id(db: Session, info: schemas.SetTgId):
    db_employee = await get_employee_by_id(db, employee_id=info.entity_id)
    setattr(db_employee, 'tg_id', info.tg_id)
    db.add(db_employee)
    db.commit()
    return 'success'


async def set_transport_company_owner_tg_id(db: Session, info: schemas.SetTgId):
    db_tc_owner = await get_employee_by_id(db, employee_id=info.entity_id)
    setattr(db_tc_owner, 'tg_id', info.tg_id)
    db.add(db_tc_owner)
    db.commit()
    return 'success'


async def get_all_info_by_tg_id(db: Session, tg_id: int):
    db_user = await get_user_by_tg_id(db, tg_id=tg_id)
    operations = await get_operations_by_user_id(db, user_id=db_user.id)
    card_numbers = db_user.cards
    balance = db_user.balance
    re_object = {
        "card_number": card_numbers,
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


async def get_next_card_number(db: Session):
    last_card = db.query(models.LastCardNumber).first()
    if last_card:
        card_number = last_card.card_number
        new_card_number = str(int(card_number) + 1)
        len_new = len(new_card_number)
        if len_new < 9:
            new_card_number = (9 - len_new) * ' ' + new_card_number
        setattr(last_card, 'card_number', new_card_number)
    else:
        new_card_number = '100000000'
        last_card = models.LastCardNumber(card_number=new_card_number)
    db.add(last_card)
    db.commit()
    return await set_luhn(new_card_number)


async def create_card(db: Session, card: schemas.CardCreate):
    db_card = models.Card(
        card_number= await get_next_card_number(db),
        owner_id=card.owner_id,
    )
    db.add(db_card)
    db.commit()
    db.refresh(db_card)
    db_user = await get_user_by_id(db, card.owner_id)
    cards = db_user.cards if db_user.cards else []
    cards.append(db_card.card_number)
    db_user.cards = cards
    flag_modified(db_user, 'cards')
    db.commit()
    return db_card.card_number


async def get_cards(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Card).offset(skip).limit(limit).all()


async def get_card_by_number(db: Session, card_number: str):
    return db.query(models.Card).filter(models.Card.card_number == card_number).first()


async def get_card_by_id(db: Session, card_id: int):
    return db.query(models.Card).filter(models.Card.id == card_id).first()


async def update_card(db: Session, card: schemas.CardUpdate, card_id: int):
    db_card = await get_card_by_id(db, card_id=card_id)
    card_data = card.dict()

    for key, value in card_data.items():
        setattr(db_card, key, value)
    db.add(db_card)
    db.commit()
    return db_card


async def delete_card(db: Session, card_id: int):
    db_card = get_card_by_id(db, card_id=card_id)

    db.delete(db_card)
    db.commit()


async def create_transport_company_owner(db: Session, owner: schemas.TCOwnerCreate):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', owner.password.encode('utf-8'), salt, 100000, dklen=128)
    db_tc_owner = models.TCOwner(
        name=owner.name,
        surname=owner.surname,
        login=owner.login,
        salt=salt.hex(),
        key=key.hex(),
        phone_number=owner.phone_number,
        role='Owner',
        )
    db.add(db_tc_owner)
    db.commit()
    db.refresh(db_tc_owner)
    return db_tc_owner.id


async def get_transport_company_owner_by_id(db: Session, owner_id: int):
    return db.query(models.TCOwner).filter(models.TCOwner.id == owner_id).first()


async def update_transport_company_owner(db: Session, owner: schemas.TCOwnerUpdate, owner_id: int):
    db_owner = await get_transport_company_owner_by_id(db, owner_id=owner_id)
    owner_data = owner.dict()

    for key, value in owner_data.items():
        setattr(db_owner, key, value)
    db.add(db_owner)
    db.commit()
    return db_owner


async def get_transport_companies_owners(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TCOwner).offset(skip).limit(limit).all()


async def get_transport_company_owner_by_name(db: Session, owner_name: str):
    return db.query(models.TCOwner).filter(models.TCOwner.name == owner_name).first()


async def login_transport_company_owner(db: Session, login: str, password: str):
    db_tc_owner = db.query(models.TCOwner).filter(models.TCOwner.login == login).first()
    if db_tc_owner is None:
        return 'numb'
    salt = bytes.fromhex(db_tc_owner.salt)
    key = bytes.fromhex(db_tc_owner.key)
    new_key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        100000,
        dklen=128)
    if new_key == key:
        return db_tc_owner
    return 'inc'


async def delete_transport_company_owner(db: Session, owner_id: int):
    db_tc_owner = await get_transport_company_owner_by_id(db, owner_id=owner_id)

    db.delete(db_tc_owner)
    db.commit()


async def get_income_by_terminal(db: Session, term_id: int):
    income = 0
    operations = await get_operations_by_terminal_id(db, term_id)
    for i in operations:
        income -= i.balance_change
    return income


async def get_transport_company_income_by_id(db: Session, tc_id: int):
    company = await get_transport_company_by_id(db, tc_id=tc_id)
    terminals = await get_terminals_by_company(db, company.name)
    income = 0
    for i in terminals:
        income += await get_income_by_terminal(db, term_id=i.terminal_id)
    return income


async def create_bus(db: Session, bus: schemas.BusCreate):
    db_bus = models.Bus(
        number=bus.number,
        company_name=bus.company_name,
        terminal_id=bus.terminal_id,
        route=bus.route,
    )
    db.add(db_bus)
    db.commit()
    db.refresh(db_bus)
    return db_bus.id


async def get_bus_by_id(db: Session, bus_id: int) -> object:
    return db.query(models.Bus).filter(models.Bus.id == bus_id).first()


async def update_bus(db: Session, bus: schemas.BusUpdate, bus_id: int):
    db_bus = await get_bus_by_id(db, bus_id=bus_id)
    bus_data = bus.dict()

    for key, value in bus_data.items():
        setattr(db_bus, key, value)
    db.add(db_bus)
    db.commit()
    return db_bus


async def get_buses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bus).offset(skip).limit(limit).all()


async def get_buses_by_company_name(db: Session, company_name: str):
    return list(db.query(models.Bus).filter(models.Bus.company_name == company_name))


async def delete_bus(db: Session, bus_id: int):
    db_bus = await get_bus_by_id(db, bus_id=bus_id)

    db.delete(db_bus)
    db.commit()


async def get_bus_by_number(db: Session, bus_number: str) -> object:
    return db.query(models.Bus).filter(models.Bus.number == bus_number).first()


async def create_route(db: Session, route: schemas.RouteCreate):
    db_route = models.Route(
        transport_company=route.transport_company,
        name = route.name,
        stops = route.stops,
        terminal_id = route.terminal_id,
        bus_number = route.bus_number,
    )
    db.add(db_route)
    db.commit()
    db.refresh(db_route)
    return db_route.id


async def get_route_by_id(db: Session, route_id: int):
    return db.query(models.Route).filter(models.Route.id == route_id).first()


async def update_route(db: Session, route: schemas.RouteUpdate, route_id: int):
    db_route = await get_route_by_id(db, route_id=route_id)
    route_data = route.dict()

    for key, value in route_data.items():
        setattr(db_route, key, value)
    db.add(db_route)
    db.commit()
    return db_route


async def delete_route(db: Session, route_id: int):
    db_route = await get_route_by_id(db, route_id=route_id)

    db.delete(db_route)
    db.commit()


async def get_route_by_name(db: Session, route_name: str):
    return db.query(models.Route).filter(models.Route.name == route_name).first()


async def get_routes_by_company_name(db: Session, company_name: str):
    return list(db.query(models.Route).filter(models.Route.transport_company == company_name))


async def get_routes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Route).offset(skip).limit(limit).all()


async def create_discrepancy(db: Session, cashier_id: int, cashbox_number: int, discrepancy: float):
    db_discrepancy = models.Discrepancy(
        date=datetime.now(),
        cashier_id = cashier_id,
        cashbox_number = cashbox_number,
        discrepancy = discrepancy,
    )
    db.add(db_discrepancy)
    db.commit()
    db.refresh(db_discrepancy)


async def create_last_check(db: Session, fact_balance: float, cashbox_number: int, cashier_balance: float, cashier_id: int):
    db_last_check = models.LastCashCheck(
        datetime=datetime.now(),
        cashier_id=cashier_id,
        cashbox_number=cashbox_number,
        fact_balance=fact_balance,
        cashier_balance=cashier_balance,
    )
    db.add(db_last_check)
    db.commit()
    db.refresh(db_last_check)


async def get_last_discrepancy(db: Session, cashbox_number: int):
    db_discrepancy = (db.query(models.Discrepancy)
                      .filter(models.Discrepancy.cashbox_number == cashbox_number)
                      .order_by(models.Discrepancy.id.desc()).first())
    if db_discrepancy:
        return db_discrepancy.discrepancy
    return None


async def check_operations(db: Session, cashbox_info: schemas.CheckOperations):
    start_fact = 0
    start_cashier = 0
    now = datetime.now()
    last_check = db.query(models.LastCashCheck).filter(
        models.LastCashCheck.cashbox_number == cashbox_info.cashbox_number
    ).first()
    if last_check:
        start_fact = last_check.fact_balance
        start_cashier = last_check.cashier_balance
        delta_time = datetime.now - last_check.datetime

        operations = list(db.query(models.Operation).filter(
            models.Operation.cashbox_number == cashbox_info.cashbox_number,
            models.Operation.cashier_id == cashbox_info.cashier_id,
            (now - models.Operation.datetime) < delta_time
        ))
    else:
        operations = list(db.query(models.Operation).filter(
            models.Operation.cashbox_number == cashbox_info.cashbox_number,
            models.Operation.cashier_id == cashbox_info.cashier_id
        ))
    fact_balance = start_fact
    if operations:
        for i in operations:
            fact_balance += i.balance_change
    if fact_balance != cashbox_info.cashbox_balance:
        discrepancy = cashbox_info.cashbox_balance - fact_balance
        last_discrepancy = await get_last_discrepancy(db, cashbox_info.cashbox_number)
        if last_discrepancy:
            if discrepancy - last_discrepancy > 0 or discrepancy - last_discrepancy < 0:
                await create_discrepancy(db, last_check.cashier_id, cashbox_info.cashbox_number,
                                         discrepancy - last_discrepancy)
        else:
            await create_discrepancy(db, last_check.cashier_id, cashbox_info.cashbox_number,
                                     discrepancy - last_discrepancy)
    await create_last_check(db, fact_balance, cashbox_info.cashbox_number, cashbox_info.cashbox_balance,
                            cashbox_info.cashier_id)
