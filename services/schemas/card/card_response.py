from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .card_request import Card


class CardNumber(BaseModel):
    card_number: str


class ReturnCard(Card):
    pass

class SuccessfulDeletion(BaseModel):
    status: str
    message: str
