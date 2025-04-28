from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class BusBase(BaseModel):
    number: str
    company_name: str
    terminal_id: int
    route: str


class BusCreate(BusBase):
    pass


class BusUpdate(BusBase):
    pass


class Bus(BusBase):
    id: int