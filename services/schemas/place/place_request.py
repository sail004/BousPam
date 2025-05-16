from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class PlaceBase(BaseModel):
    name: str
    address: str
    status: str = Field(default="inactive", description='One of 2 statuses: active, inactive')

    @field_validator('status')
    @classmethod
    def validate_status(cls, values):
        if values not in ['active', 'inactive']:
            raise ValueError("Status should be one of 'active', 'inactive'")
        return values


class PlaceCreate(PlaceBase):
    pass


class PlaceUpdate(PlaceBase):
    pass


class Place(PlaceBase):
    id: int
