from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .user_request import User


class ReturnId(BaseModel):
    id: int | None = None
    msg: str = 'successful'


class ReturnUser(User):
    cards: list[str] | None = None
    tg_id: int | None = None


class ReturnBalance(BaseModel):
    balance: float


class SuccessfulDeletion(BaseModel):
    status: str
    message: str
