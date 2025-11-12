from typing import List, Optional
from pydantic import BaseModel
from datetime import date, datetime

class MedicalRecord(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    hospital_id: Optional[int] = None
    hospital_name: Optional[str] = None
    diagnosis: str
    treatment: str
    notes: Optional[str] = None
    follow_up_date: Optional[date] = None
    created_by: Optional[str] = None
    record_date: date = datetime.utcnow().date()
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class PrescriptionInfo(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    record_id: Optional[int] = None
    hospital_id: Optional[int] = None
    hospital_name: Optional[str] = None
    medicine_name: str
    frequency: Optional[str] = None
    duration: str
    notes: Optional[str] = None
    dosage: str
    prescription_details: Optional[str] = None
    prescribed_by: Optional[str] = None
    prescription_date: date = datetime.utcnow().date()
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

class LabTestInfo(BaseModel):
    patient_id: Optional[int] = None
    doctor_id: Optional[int] = None
    record_id: Optional[int] = None
    hospital_id: Optional[int] = None
    hospital_name: Optional[str] = None
    test_name: str
    result_value: str
    result_date: date = datetime.utcnow().date()
    notes: Optional[str] = None
    doctor_name: Optional[str] = None
    files: list = []
    created_at: datetime = datetime.utcnow()
    updated_at: datetime = datetime.utcnow()

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
