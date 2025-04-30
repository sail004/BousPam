from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .terminal_request import Terminal


class SuccessfulDeletion(BaseModel):
    status: str
    message: str

class ReturnTerminal(Terminal):
    pass
