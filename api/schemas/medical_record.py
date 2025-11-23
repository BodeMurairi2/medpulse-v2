#!/usr/bin/env python3
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field

# -------------------------------
# Medical Record Model
# -------------------------------
class MedicalRecord(BaseModel):
    """Represents a single medical record of a patient."""
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    hospital_id: Optional[int] = Field(None, title="Hospital ID")
    hospital_name: Optional[str] = Field(None, title="Hospital Name")
    diagnosis: str = Field(..., title="Enter diagnosis")
    treatment: str = Field(..., title="Enter treatment")
    notes: Optional[str] = Field(None, title="Doctor notes")
    follow_up_date: Optional[date] = Field(None, title="Follow-up date")
    created_by: str = Field(..., title="Doctor Name who created the record")
    record_date: date = Field(default_factory=lambda: datetime.utcnow().date())
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------
# Prescription Info Model
# -------------------------------
class PrescriptionInfo(BaseModel):
    """Represents a prescription given to a patient."""
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    record_id: Optional[int] = None
    hospital_id: Optional[int] = None
    hospital_name: Optional[str] = None
    medicine_name: str = Field(..., title="Medicine Name")
    frequency: str = Field(..., title="Dosage Frequency")
    duration: str = Field(..., title="Duration of the medicine")
    dosage: str = Field(..., title="Dosage Information")
    notes: Optional[str] = None
    prescription_details: Optional[str] = None
    prescribed_by: str = Field(..., title="Doctor who prescribed the medicine")
    prescription_date: date = Field(default_factory=lambda: datetime.utcnow().date())
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------
# Lab Test Info Model
# -------------------------------
class LabTestInfo(BaseModel):
    """Represents a lab test done for a patient."""
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    record_id: Optional[int] = None
    hospital_id: Optional[int] = None
    hospital_name: Optional[str] = None
    test_name: str = Field(..., title="Name of the lab test")
    result_value: str = Field(..., title="Results of the lab test")
    result_date: date = Field(default_factory=lambda: datetime.utcnow().date())
    notes: Optional[str] = None
    doctor_name: str = Field(..., title="Doctor who ordered the test")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------
# Lab Test File Info Model
# -------------------------------
class LabTestFileInfo(BaseModel):
    """Represents files attached to a lab test."""
    lab_test_id: int
    file_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# -------------------------------
# Patient Records Output Model
# -------------------------------
class PatientRecordsOut(BaseModel):
    """Aggregated patient record output including medical records, prescriptions, and lab tests."""
    id: int
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    medical_records: List[MedicalRecord] = Field(default_factory=list)
    prescriptions: List[PrescriptionInfo] = Field(default_factory=list)
    lab_tests: List[LabTestInfo] = Field(default_factory=list)

    class Config:
        orm_mode = True
        # For Pydantic v2, you can also use:
        # from_attributes = True
