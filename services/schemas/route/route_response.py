from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .route_request import Route


class ReturnId(BaseModel):
    id: int | None = None
    msg: str | None = None


class ReturnRoute(Route):
    pass


class SuccessfulDeletion(BaseModel):
    status: str
    message: str
