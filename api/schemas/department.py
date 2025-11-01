#!/usr/bin/env python3

import re
from pydantic import BaseModel, Field, EmailStr, field_validator
from datetime import datetime

class Department(BaseModel):
    """Pydantic object for Department"""
    department_name: str = Field(..., title="Department Name", min_length=3, max_length=50)
    department_description:str = Field(..., title="Department Description", min_length=10, max_length=400)
    department_email: EmailStr = Field(..., title="Department Email", description="A valid email address for the department")
    hospital_id:int
    phone: str = Field(..., title="Department Phone", min_length=7, max_length=15)
    location: str = Field(..., title="Department Location", min_length=5, max_length=150)
    number_of_staff: int = Field(..., title="Number of Staff in Department", gt=1)
    status: bool = Field(..., title="Department Status", description="Indicates if the department is active or inactive")
    created_at: datetime = Field(default_factory=datetime.utcnow, title="Creation Timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, title="Last Update Timestamp")

    @field_validator('phone')
    def validate_phone(cls, phone):
        pattern = re.compile(r"^\+?\d[\d\s\-\(\)]{6,14}\d$")
        if not pattern.match(phone):
            raise ValueError("Phone number must be valid, digits with optional +, spaces, hyphens, or parentheses")
        return phone
