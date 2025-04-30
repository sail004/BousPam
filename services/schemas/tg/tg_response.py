from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class ReturnInfo(BaseModel):
    card_number: str | None = None
    balance: float | None = None
    operations: list | None = None


class ReturnUser(BaseModel):
    name: str
    surname: str
    phone_number: str
    e_mail: str
    passport_number: str
    niu: str
    nif: str
    cards: list[str]
    tg_id: int
    id: int
    balance: float


class ReturnSuccess(BaseModel):
    msg: str


class ReturnOperations(BaseModel):
    operations: list


class ReturnBalance(BaseModel):
    balance: float
