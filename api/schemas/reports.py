from datetime import date, datetime
from typing import List, Optional
from enum import Enum
from pydantic import BaseModel

class ReportType(str, Enum):
    PATIENTS = "patients"
    DOCTORS = "doctors"
    APPOINTMENTS = "appointments"

# Patient Schemas
class PatientReportRequest(BaseModel):
    start_date: date
    end_date: date
    department: Optional[str] = None

class PatientSummary(BaseModel):
    patient_id: int
    first_name: str
    second_name: str
    age: int
    gender: str
    contact: str
    last_visit: Optional[date]
    total_visits: int

class PatientReportResponse(BaseModel):
    report_type: str = "patients"
    generated_at: datetime
    period: str
    total_patients: int
    new_patients: int
    patients: List[PatientSummary]

# Doctor Schemas
class DoctorReportRequest(BaseModel):
    start_date: date
    end_date: date
    department: Optional[str] = None

class DoctorSummary(BaseModel):
    doctor_id: int
    full_name: str
    specialization: str
    department: str
    total_appointments: int
    completed_appointments: int
    cancelled_appointments: int
    total_patients_seen: int

class DoctorReportResponse(BaseModel):
    report_type: str = "doctors"
    generated_at: datetime
    period: str
    total_doctors: int
    doctors: List[DoctorSummary]

# Appointment Schemas
class AppointmentReportRequest(BaseModel):
    start_date: date
    end_date: date
    status: Optional[str] = None
    department: Optional[str] = None

class AppointmentSummary(BaseModel):
    appointment_id: int
    appointment_date: datetime
    patient_name: str
    doctor_name: str
    department: str
    status: str
    notes: Optional[str]

class AppointmentReportResponse(BaseModel):
    report_type: str = "appointments"
    generated_at: datetime
    period: str
    total_appointments: int
    completed: int
    cancelled: int
    scheduled: int
    no_show: int
    appointments: List[AppointmentSummary]