from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .operations_request import Operation


class ReturnOperation(Operation):
    id_terminal: int | None = None
    terminal_hash: str | None = None
    request_time: datetime | None = None
    cashier_id: int | None = None
    cashbox_number: int | None = None
    balance_change: float | None = None


class ReturnBalance(BaseModel):
    balance: float
