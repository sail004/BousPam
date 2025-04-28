from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .company_request import TransportCompany


class ReturnId(BaseModel):
    id: int | None = None
    message: str | None = None


class ReturnCompany(TransportCompany):
    pass


class ReturnCompanyJoined(BaseModel):
    id: int
    name: str
    owner_number: str
    owner: str


class SuccessfulDeletion(BaseModel):
    status: str
    message: str
