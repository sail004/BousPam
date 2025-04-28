from __future__ import annotations
from enum import Enum, StrEnum
from pydantic import BaseModel, Field, field_validator, ValidationError
from datetime import datetime


class EmployeeBase(BaseModel):
    name: str
    surname: str
    password: str
    role: str = Field(default=..., description='One of 3 roles: Admin, Cashier, Owner')
    login: str
    gender: str
    date_of_birth: str
    phone_number: str

    @field_validator('role')
    @classmethod
    def validate_role(cls, values):
        if values not in ['Admin', 'Cashier', 'Owner']:
            raise ValueError("Role should be one of 'Admin', 'Cashier', 'Owner'")
        return values


class EmployeeCreate(EmployeeBase):
    pass


class EmployeeUpdate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: int
    salt: str
    key: str