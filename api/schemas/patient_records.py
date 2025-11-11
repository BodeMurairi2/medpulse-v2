from pydantic import BaseModel
from datetime import datetime, date
from typing import List, Optional

class DepartmentBase(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    class Config:
        orm_mode = True

class ConsultationOut(BaseModel):
    doctor_name: Optional[str] = None
    department_name: Optional[str] = None
    date: datetime
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class PrescriptionOut(BaseModel):
    medication: str
    dosage: Optional[str] = None
    duration: Optional[str] = None
    date_issued: datetime

    class Config:
        orm_mode = True


class LabTestOut(BaseModel):
    test_name: str
    result: Optional[str] = None
    reference_range: Optional[str] = None
    date_conducted: datetime

    class Config:
        orm_mode = True


class AppointmentOut(BaseModel):
    doctor_name: Optional[str] = None
    department_name: Optional[str] = None
    appointment_date: datetime
    status: str
    notes: Optional[str] = None

    class Config:
        orm_mode = True


class PatientRecordsOut(BaseModel):
    id: int
    full_name: str
    gender: str
    contact: str
    email: Optional[str] = None
    date_of_birth: date
    consultations: List[ConsultationOut] = []
    prescriptions: List[PrescriptionOut] = []
    lab_tests: List[LabTestOut] = []
    appointments: List[AppointmentOut] = []

    class Config:
        orm_mode = True
