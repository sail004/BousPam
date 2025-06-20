from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class TerminalBase(BaseModel):
    company: str
    fare: int


class Terminal(TerminalBase):
    terminal_id: int
    hash: str


class TerminalCreate(TerminalBase):
    pass


class TerminalUpdate(TerminalBase):
    pass
