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
