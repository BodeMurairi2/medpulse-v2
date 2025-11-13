#!/usr/bin/env python3
from typing import List, Optional
from datetime import date, datetime
from pydantic import BaseModel, Field

class MedicalRecord(BaseModel):
    patient_id: int
    doctor_id: int
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

class PrescriptionInfo(BaseModel):
    patient_id: int
    doctor_id: int
    record_id: Optional[int] = None
    hospital_id: Optional[int] = None
    hospital_name: Optional[str] = Field(None, title="Hospital Name")
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
    hospital_id: Optional[int] = None
    hospital_name: Optional[str] = Field(None, title="Hospital Name")
    test_name: str = Field(..., title="Name of the lab test")
    result_value: str = Field(..., title="Results of the lab test")
    result_date: date = Field(default_factory=lambda: datetime.utcnow().date())
    notes: Optional[str] = Field(None, title="Additional notes about the test")
    doctor_name: str = Field(..., title="Doctor who ordered the test")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class LabTestFileInfo(BaseModel):
    lab_test_id: int
    file_url: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

class PatientRecordsOut(BaseModel):
    id: int
    full_name: str
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    contact: Optional[str] = None
    email: Optional[str] = None
    medical_records: List[MedicalRecord] = []
    prescriptions: List[PrescriptionInfo] = []
    lab_tests: List[LabTestInfo] = []

    class Config:
        orm_mode = True