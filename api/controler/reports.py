from fastapi import APIRouter
from schemas.reports import (
    PatientReportRequest, PatientReportResponse,
    DoctorReportRequest, DoctorReportResponse,
    AppointmentReportRequest, AppointmentReportResponse
)
from services.reports import (
    generate_patient_report,
    generate_doctor_report,
    generate_appointment_report
)

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("/patients", response_model=PatientReportResponse)
def get_patient_report(request: PatientReportRequest):
    """Generate patient report for specified date range"""
    return generate_patient_report(request)

@router.post("/doctors", response_model=DoctorReportResponse)
def get_doctor_report(request: DoctorReportRequest):
    """Generate doctor performance report for specified date range"""
    return generate_doctor_report(request)

@router.post("/appointments", response_model=AppointmentReportResponse)
def get_appointment_report(request: AppointmentReportRequest):
    """Generate appointment report for specified date range"""
    return generate_appointment_report(request)