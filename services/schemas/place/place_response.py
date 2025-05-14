from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime
from .place_request import Place


class ReturnPlace(Place):
    pass


class SuccessfulDeletion(BaseModel):
    status: str
    message: str
