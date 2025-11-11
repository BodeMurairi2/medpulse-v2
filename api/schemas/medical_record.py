#!/usr/bin/env python3

from typing import Optional
from datetime import datetime, date
from pydantic import BaseModel, field_validator, Field

class MedicalRecord(BaseModel):
    """Pydantic model for medical record creation"""
    patient_id: int
    doctor_id: int
    hospital_id: int
    hospital_name: str = Field(..., title="Hospital Name")
    diagnosis: str = Field(..., title="Enter diagnosis")
    treatment: str = Field(..., title="Enter treatment")
    notes: str = Field(..., title="Doctor notes")
    follow_up_date: Optional[date] = Field(None, title="Follow-up date")
    created_by: str = Field(..., title="Doctor Name who created the record")
    record_date: date = Field(default_factory=lambda: datetime.utcnow().date())
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class PrescriptionInfo(BaseModel):
    patient_id: int
    doctor_id: int
    record_id: Optional[int] = None
    hospital_id: int
    hospital_name: str = Field(..., title="Hospital Name")
    medicine_name: str = Field(..., title="Medicine Name")
    frequency: str = Field(..., title="Dosage Frequency")
    duration: str = Field(..., title="Duration of the medicine")
    notes: Optional[str] = Field(None, title="Additional notes")
    dosage: str = Field(..., title="Dosage Information")
    prescription_details: Optional[str] = Field(None, title="Details about the prescription")
    prescribed_by: str = Field(..., title="Doctor who prescribed the medicine")
    prescription_date: date = Field(default_factory=lambda: datetime.utcnow().date())
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class LabTestInfo(BaseModel):
    patient_id: int
    doctor_id: int
    record_id: Optional[int] = None
    hospital_id: int
    hospital_name: str = Field(..., title="Hospital Name")
    test_name: str = Field(..., title="Name of the lab test")
    result_value: str = Field(..., title="Results of the lab test")
    result_date: date = Field(default_factory=lambda: datetime.utcnow().date())
    notes: Optional[str] = Field(None, title="Additional notes about the test")
    doctor_name: str = Field(..., title="Doctor who ordered the test")
    attached_files: Optional[str] = Field(None, title="File path or URL to the test result")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
