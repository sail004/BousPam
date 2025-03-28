from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    name: str
    surname: str
    phone_number: str
    e_mail: str
    passport_number: str
    card_number: str
    snils: str
    inn: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    tg_id: int


class User(UserBase):
    id: int
    balance: float
    

class OperationBase(BaseModel):
    id_user: int


class Operation(OperationBase):
    id_operation: int
    balance_change: float
    type: str
    datetime: datetime


class OperationPaymentCreate(OperationBase):
    id_terminal: int
    terminal_hash: str
    request_time: datetime


class OperationReplenishmentCreate(OperationBase):
    balance_change: float


class OperationUpdate(OperationBase):
    pass


class TerminalBase(BaseModel):
    company_name: str
    fare: int


class Terminal(TerminalBase):
    terminal_id: int
    hash: str


class TerminalCreate(TerminalBase):
    pass


class TerminalUpdate(TerminalBase):
    pass


class TransportCompanyBase(BaseModel):
    name: str
    owner_name: str
    owner_surname: str


class TransportCompany(TransportCompanyBase):
    id: int


class TransportCompanyCreate(TransportCompanyBase):
    pass


class TransportCompanyUpdate(TransportCompanyBase):
    pass


class EmployeeBase(BaseModel):
    name: str
    surname: str
    password: str
    role: str
    login: str
    gender: str
    date_of_birth: str
    phone_number: str


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    salt: str
    key: str


class Card(BaseModel):
    number: str


class Login(BaseModel):
    login: str
    password: str
