from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class ReturnOwnerOrEmployee(BaseModel):
    msg: str | None = None
    name: str | None = None
    surname: str | None = None
    role: str | None = Field(default=None, description='One of 3 roles: Admin, Cashier, Owner')
    gender: str | None = None
    date_of_birth: str | None = None
    phone_number: str | None = None
    salt: str | None = None
    key: str | None = None
    id: int | None = None
    company_id: int | None = None


class SuccessfulLogout(BaseModel):
    message: str
