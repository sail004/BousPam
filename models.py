from sqlalchemy import Column, Integer, String, Float, DateTime, ARRAY
import schemas
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    password = Column(String)
    surname = Column(String)
    phone_number = Column(String)
    balance = Column(Float)
    e_mail = Column(String)
    passport_number = Column(String)
    snils = Column(String)
    inn = Column(String)

class Operation(Base):
    __tablename__ = "operations"

    id_operation = Column(Integer, primary_key=True)
    id_terminal = Column(Integer)
    id_user = Column(Integer)
    balance_change = Column(Float)
    datetime = Column(DateTime)

class Terminal(Base):
    __tablename__ = "terminals"

    id = Column(Integer, primary_key=True)
    transport_company = Column(String)
    route = Column(String)

class TransportCompany(Base):
    __tablename__ = "transport_companies"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    routes = Column(String)
    terminals = Column(String)

class Route(Base):
    __tablename__ = "routes"
    id = Column(Integer, primary_key=True)
    transport_company = Column(String)
    name = Column(String)
    stops = Column(String)

