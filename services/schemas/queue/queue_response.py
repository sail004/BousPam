from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class ReturnQueue(BaseModel):
    id: int
    status: str = Field(default="free", description='One of 2 statuses: free, occupied')
    datetime: datetime
    passenger_id: int
    type: str
    place: str

    @field_validator('status')
    @classmethod
    def validate_status(cls, values):
        if values not in ['free', 'occupied']:
            raise ValueError("Status should be one of 'free', 'occupied'")
        return values


class Message(BaseModel):
    msg: str


class SuccessfulDeletion(BaseModel):
    status: str
    message: str
