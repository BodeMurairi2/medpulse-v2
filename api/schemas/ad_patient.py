#!/usr/bin/env python3

from datetime import date, datetime
from typing import Literal, Optional
from pydantic import BaseModel, EmailStr, Field

class PatientInfo(BaseModel):
    """Pydantic model for patient"""
    first_name: str = Field(..., title="Patient first name", min_length=2, max_length=30)
    middle_name: Optional[str] = Field(None, title="Patient middle name", min_length=2, max_length=30)
    second_name: str = Field(..., title="Patient last name", min_length=2, max_length=25)
    id_type: Literal["National ID", "Passport", "Driver's License", "Other"]
    gender: Literal["Male", "Female"]
    date_of_birth: date
    home_address: str = Field(..., title="Home Address", min_length=5, max_length=200)
    phone_number: str = Field(..., title="Patient Phone", min_length=7, max_length=15)
    email: EmailStr = Field(..., title="Patient Email")
    password_hash: str = Field(..., title="Password Hash")
    emergency_contact_name: str = Field(..., title="Emergency contact name", min_length=2, max_length=30)
    emergency_contact_phone: str = Field(..., title="Emergency contact phone", min_length=7, max_length=15)
    profile_picture: Optional[str] = Field(None, title="Profile Picture URL")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
