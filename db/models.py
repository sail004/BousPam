from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.dialects.postgresql import ARRAY
from db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    phone_number = Column(String)
    balance = Column(Float)
    e_mail = Column(String)
    passport_number = Column(String)
    niu = Column(String)
    nif = Column(String)
    cards = Column(ARRAY(String))
    tg_id = Column(Integer)

class Operation(Base):
    __tablename__ = "operations"

    id_operation = Column(Integer, primary_key=True)
    id_terminal = Column(Integer)
    terminal_hash = Column(String)
    id_user = Column(Integer)
    type = Column(String)
    balance_change = Column(Float)
    datetime = Column(DateTime)
    cashier_id = Column(Integer)
    cashbox_number = Column(Integer)

class Terminal(Base):
    __tablename__ = "terminals"

    terminal_id = Column(Integer, primary_key=True)
    company = Column(String)
    fare = Column(Integer)
    hash = Column(String)

class TransportCompany(Base):
    __tablename__ = "transport_companies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    owner_name = Column(String)
    owner_surname = Column(String)
    owner_number = Column(String)
    owner_id = Column(Integer)

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    login = Column(String)
    key = Column(String)
    salt = Column(String)
    gender = Column(String)
    date_of_birth = Column(String)
    phone_number = Column(String)
    role = Column(String)
    tg_id = Column(String)

class StopList(Base):
    __tablename__ = "stoplist"

    id = Column(Integer, primary_key=True)
    card_number = Column(String)
    owner_id = Column(Integer)
    owner_phone_number = Column(String)

class Card(Base):
    __tablename__ = "cards"

    id = Column(Integer, primary_key=True)
    card_number = Column(String)
    owner_id = Column(Integer)

class LastCardNumber(Base):
    __tablename__ = "lastcard_number"

    id = Column(Integer, primary_key=True)
    card_number = Column(String)

class TCOwner(Base):
    __tablename__ = "tc_owners"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    login = Column(String)
    key = Column(String)
    salt = Column(String)
    role = Column(String)
    phone_number = Column(String)
    company_id = Column(Integer)
    tg_id = Column(String)

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True)
    number = Column(String)
    company_name = Column(String)
    route = Column(String)
    terminal_id = Column(Integer)

class Route(Base):
    __tablename__ = "routes"

    id = Column(Integer, primary_key=True)
    transport_company = Column(String)
    name = Column(String)
    stops = Column(ARRAY(String))
    terminal_id = Column(Integer)
    bus_number = Column(String)

class Discrepancy(Base):
    __tablename__ = "discrepancies"

    id = Column(Integer, primary_key=True)
    date = Column(DateTime)
    cashier_id = Column(Integer)
    cashbox_number = Column(Integer)
    discrepancy = Column(Float)

class LastCashCheck(Base):
    __tablename__ = "last_check"

    id = Column(Integer, primary_key=True)
    cashbox_number = Column(Integer)
    fact_balance = Column(Float)
    cashier_balance = Column(Float)
    datetime = Column(DateTime)
    cashier_id = Column(Integer)

class Queue(Base):
    __tablename__ = "queue"

    id = Column(Integer, primary_key=True)
    datetime = Column(DateTime)
    type = Column(String)
    place = Column(String)

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    status = Column(String)
