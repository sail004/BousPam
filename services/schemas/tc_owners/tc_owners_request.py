from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


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
