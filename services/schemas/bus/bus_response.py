from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .bus_request import Bus


class ReturnId(BaseModel):
    id: int


class ReturnBus(Bus):
    pass


class SuccessfulDeletion(BaseModel):
    status: str
    message: str
