from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .tc_owners_request import TCOwner
from services.schemas.company.company_response import ReturnCompany


class ReturnId(BaseModel):
    id: int | None = None
    msg: str | None = None


class ReturnTCOwner(TCOwner):
    pass


class ReturnIncome(BaseModel):
    income: float


class ReturnCompanyInfo(ReturnCompany):
    pass


class SuccessfulDeletion(BaseModel):
    status: str
    message: str
