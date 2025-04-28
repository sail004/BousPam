from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .employee_request import Employee


class ReturnId(BaseModel):
    id: int | None = None
    msg: str | None = None


class ReturnEmployee(BaseModel):
    name: str
    surname: str
    role: str = Field(default=..., description='One of 3 roles: Admin, Cashier, Owner')
    gender: str
    date_of_birth: str
    phone_number: str
    id: int
    salt: str
    key: str


class SuccessfulDeletion(BaseModel):
    status: str
    message: str
