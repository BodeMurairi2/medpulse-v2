#!/usr/bin/env python3
import re
from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field, EmailStr, field_validator

class DoctorClass(BaseModel):
    first_name: str = Field(..., title="Doctor first name", min_length=2, max_length=25)
    last_name: str = Field(..., title="Doctor last name", min_length=2, max_length=25)
    gender: Literal["Male", "Female"]
    department: str = Field(..., title="Department Name As registered")
    phone_number: str = Field(..., title="Doctor Phone", min_length=7, max_length=15)
    email: EmailStr = Field(..., title="Doctor Email")
    password_hash: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @field_validator('phone_number')
    def validate_phone(cls, phone):
        pattern = re.compile(r"^\+?\d[\d\s\-\(\)]{6,14}\d$")
        if not pattern.match(phone):
            raise ValueError(
                "Phone number must be valid, digits with optional +, spaces, hyphens, or parentheses"
            )
        return phone

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    gender: str | None = None
    department: str | None = None
    phone_number: str | None = None
    email: EmailStr
    password: str

class DoctorLogin(BaseModel):
    email:EmailStr
    password:str
