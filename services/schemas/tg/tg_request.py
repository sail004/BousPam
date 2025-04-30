from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class TgCard(BaseModel):
    number: str


class SetTgId(BaseModel):
    tg_id: str
    entity_id: int