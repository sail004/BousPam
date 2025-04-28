from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class TransportCompanyBase(BaseModel):
    name: str
    owner_id: int


class TransportCompany(TransportCompanyBase):
    id: int
    owner_name: str
    owner_surname: str
    owner_number: str


class TransportCompanyCreate(TransportCompanyBase):
    pass


class TransportCompanyUpdate(TransportCompanyBase):
    pass