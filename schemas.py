from __future__ import annotations
from typing import Union
from pydantic import BaseModel
from datetime import datetime


class UserBase(BaseModel):
    name: str
    surname: str
    password: str
    phone_number: str



class UserCreate(UserBase):
    password2: str


class UserUpdate(UserBase):
    e_mail: str
    passport_number: str
    snils: str
    inn: str


class User(UserBase):
    id: int
    balance: float


class OperationBase(BaseModel):
    balance_change: float
    id_user: int


class Operation(OperationBase):
    id_operation: int
    type: str
    datetime: datetime


class OperationPaymentCreate(OperationBase):
    id_terminal: int


class OperationReplenishmentCreate(OperationBase):
    bank_name: str


class OperationUpdate(OperationBase):
    pass


class TerminalBase(BaseModel):
    transport_company: str
    route: str


class Terminal(TerminalBase):
    id: int


class TerminalCreate(TerminalBase):
    pass


class TerminalUpdate(TerminalBase):
    pass


class RouteBase(BaseModel):
    transport_company: str
    name: str
    stops: str


class RouteCreate(RouteBase):
    pass


class RouteUpdate(RouteBase):
    pass


class Route(RouteBase):
    id: int


class TransportCompanyBase(BaseModel):
    name: str
    routes: str
    terminals: str


class TransportCompany(TransportCompanyBase):
    id: int


class TransportCompanyCreate(TransportCompanyBase):
    pass


class TransportCompanyUpdate(TransportCompanyBase):
    pass
