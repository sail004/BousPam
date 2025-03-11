from __future__ import annotations
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    name: str
    surname: str
    password: str
    phone_number: str



class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    e_mail: str
    passport_number: str
    snils: str
    inn: str


class User(UserBase):
    id: int
    salt: str
    key: str
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
    bank_name: str


class OperationUpdate(OperationBase):
    pass


class TerminalBase(BaseModel):
    transport_company: str
    price: int


class Terminal(TerminalBase):
    id: int
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
