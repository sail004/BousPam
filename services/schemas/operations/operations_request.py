from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


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


class StopListBase(BaseModel):
    card_number: str


class StopListCreate(StopListBase):
    owner_id: int
    owner_phone_number: str


class StopListUpdate(StopListBase):
    pass


class StopList(StopListBase):
    id: int


class CheckOperations(BaseModel):
    cashier_id: int
    cashbox_number: int
    cashbox_balance: float
