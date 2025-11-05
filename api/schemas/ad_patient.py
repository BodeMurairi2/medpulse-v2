#!/usr/bin/env python3

import re
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Literal
from datetime import datetime

class PatientInfo(BaseModel):
    """Pydantic model for patient"""
    first_name: str = Field(..., title="Patient first name", min_length=2, max_length=30)
    middle_name: str = Field(..., title="Patient middle name", min_length=2, max_length=30)
    second_name: str = Field(..., title="Patient last name", min_length=2, max_length=25)
    gender: Literal["Male", "Female"]
    date_of_birth:datetime
    home_address:str = Field(..., title="Home Address", min_length=5, max_length=200)
    phone_number: str = Field(..., title="Doctor Phone", min_length=7, max_length=15)
    email:EmailStr = Field(..., title="Patient Email")
    emergency_contact_name:str= Field(..., title="Emergency contact name", min_length=2, max_length=30)
    emergency_contact_phone:str = Field(..., title="Emergency contact email", min_length=7, max_length=15)
    profile_picture:str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
