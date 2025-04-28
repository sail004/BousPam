from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class Login(BaseModel):
    login: str
    password: str
