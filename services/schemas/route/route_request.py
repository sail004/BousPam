from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class RouteBase(BaseModel):
    transport_company: str
    name: str
    stops: list[str] = Field(..., description="Should be at least 2 stops")
    terminal_id: int
    bus_number: str

    @field_validator('stops')
    @classmethod
    def validate_stops(cls, values):
        if len(values) < 2:
            raise ValueError("Should be at least 2 stops")
        return values


class RouteCreate(RouteBase):
    pass


class RouteUpdate(RouteBase):
    pass


class Route(RouteBase):
    id: int