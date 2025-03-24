from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    phone_number = Column(String)
    balance = Column(Float)
    e_mail = Column(String)
    passport_number = Column(String)
    snils = Column(String)
    inn = Column(String)
    card_number = Column(String)
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

class Terminal(Base):
    __tablename__ = "terminals"

    id = Column(Integer, primary_key=True)
    transport_company = Column(String)
    price = Column(Integer)
    hash = Column(String)

class TransportCompany(Base):
    __tablename__ = "transport_companies"

    id = Column(Integer, primary_key=True)
    owner_name = Column(String)
    owner_surname = Column(String)
    name = Column(String)

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
