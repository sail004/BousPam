from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class UserBase(BaseModel):
    name: str
    surname: str
    phone_number: str
    e_mail: str
    passport_number: str
    niu: str
    nif: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    cards: list[str]
    tg_id: int


class User(UserBase):
    id: int
    balance: float
    

class OperationBase(BaseModel):
    card_number: str


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
    cashier_id: int
    cashbox_number: int
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
    owner_id: int


class TransportCompany(TransportCompanyBase):
    id: int
    owner_name: int
    owner_surname: int
    owner_number: str


class TransportCompanyCreate(TransportCompanyBase):
    pass


class TransportCompanyUpdate(TransportCompanyBase):
    pass


class EmployeeBase(BaseModel):
    name: str
    surname: str
    password: str
    role: str = Field(default=..., description='One of 3 roles: Admin, Cashier, Owner')
    login: str
    gender: str
    date_of_birth: str
    phone_number: str

    @field_validator('role')
    @classmethod
    def validate_role(cls, values):
        if values not in ['Admin', 'Cashier', 'Owner']:
            raise ValueError("Role should be one of 'Admin', 'Cashier', 'Owner'")
        return values


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    salt: str
    key: str





class StopListBase(BaseModel):
    card_number: str


class StopListCreate(StopListBase):
    owner_id: int
    owner_phone_number: str


class StopListUpdate(StopListBase):
    pass


class StopList(StopListBase):
    id: int


class TCOwnerBase(BaseModel):
    name: str
    surname: str
    password: str
    login: str
    phone_number: str


class TCOwnerCreate(TCOwnerBase):
    pass


class TCOwnerUpdate(TCOwnerBase):
    company_id: int


class TCOwner(TCOwnerBase):
    id: int
    salt: str
    key: str





class RouteBase(BaseModel):
    transport_company: str
    name: str
    stops: list[str]
    terminal_id: int
    bus_number: str

    @field_validator('stops')
    @classmethod
    def validate_stops(cls, values):
        if len(values) < 2:
            raise ValueError("Should be at least 2 stops")
        return values


class RouteCreate(RouteBase):
    pass


class RouteUpdate(RouteBase):
    pass


class Route(RouteBase):
    id: int


class TgCard(BaseModel):
    number: str


class SetTgId(BaseModel):
    tg_id: str
    entity_id: int


class CheckOperations(BaseModel):
    cashier_id: int
    cashbox_number: int
    cashbox_balance: float


class ReturnId(BaseModel):
    id: int


class SuccesfulDeletion:
    status = "ok"
    message = "Deletion was successful"
