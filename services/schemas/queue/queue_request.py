from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class OccupyPlaceInQueue(BaseModel):
    passenger_id: int
    date: datetime
    time: datetime
    place: str
    type: str = Field(..., description='The reason for the request, should be one of "getting card", "replenishment"')

    @field_validator('type')
    @classmethod
    def validate_type(cls, values):
        if values not in ['getting card', 'replenishment']:
            raise ValueError("Type should be one of 'getting card', 'replenishment'")
        return values