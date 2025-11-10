#!/usr/bin/env python3
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from data.database import get_db
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
def get_patient_report(request: PatientReportRequest, db: Session = Depends(get_db)):
    """Generate patient report for specified date range"""
    return generate_patient_report(request, db)

@router.post("/doctors", response_model=DoctorReportResponse)
def get_doctor_report(request: DoctorReportRequest, db: Session = Depends(get_db)):
    """Generate doctor performance report for specified date range"""
    return generate_doctor_report(request, db)

@router.post("/appointments", response_model=AppointmentReportResponse)
def get_appointment_report(request: AppointmentReportRequest, db: Session = Depends(get_db)):
    """Generate appointment report for specified date range"""
    return generate_appointment_report(request, db)
