#!/usr/bin/env python3

from schemas.reports import (
    PatientReportRequest, PatientReportResponse, PatientSummary,
    DoctorReportRequest, DoctorReportResponse, DoctorSummary,
    AppointmentReportRequest, AppointmentReportResponse, AppointmentSummary
)
from datetime import datetime, date

def generate_patient_report(request: PatientReportRequest) -> PatientReportResponse:
    """Generate report of patients registered/visited in the given period"""
    dummy_patients = [
        PatientSummary(
            patient_id=1,
            full_name="Faith Irakoze",
            age=22,
            gender="Female",
            contact="+250788123456",
            last_visit=date(2024, 10, 25),
            total_visits=5
        ),
        PatientSummary(
            patient_id=2,
            full_name="Karangwa Arnold",
            age=30,
            gender="Male",
            contact="+250788654321",
            last_visit=date(2024, 10, 28),
            total_visits=3
        ),
        PatientSummary(
            patient_id=3,
            full_name="Alice Teta",
            age=28,
            gender="Female",
            contact="+250788987654",
            last_visit=date(2024, 10, 20),
            total_visits=7
        )
    ]
    return PatientReportResponse(
        generated_at=datetime.now(),
        period=f"{request.start_date} to {request.end_date}",
        total_patients=len(dummy_patients),
        new_patients=1,
        patients=dummy_patients
    )

def generate_doctor_report(request: DoctorReportRequest) -> DoctorReportResponse:
    """Generate performance report for doctors in the given period"""
    dummy_doctors = [
        DoctorSummary(
            doctor_id=1,
            full_name="Dr. Amina Mugisha",
            specialization="General Medicine",
            department="General Medicine",
            total_appointments=38,
            completed_appointments=35,
            cancelled_appointments=1,
            total_patients_seen=34
        ),
        DoctorSummary(
            doctor_id=2,
            full_name="Dr. Alex Kagame",
            specialization="Cardiology",
            department="Cardiology",
            total_appointments=45,
            completed_appointments=40,
            cancelled_appointments=3,
            total_patients_seen=38
        ),
        DoctorSummary(
            doctor_id=3,
            full_name="Dr. Micheal Chen",
            specialization="Pediatrics",
            department="Pediatrics",
            total_appointments=52,
            completed_appointments=48,
            cancelled_appointments=2,
            total_patients_seen=45
        )
    ]
    return DoctorReportResponse(
        generated_at=datetime.now(),
        period=f"{request.start_date} to {request.end_date}",
        total_doctors=len(dummy_doctors),
        doctors=dummy_doctors
    )

def generate_appointment_report(request: AppointmentReportRequest) -> AppointmentReportResponse:
    """Generate report of appointments in the given period"""
    dummy_appointments = [
        AppointmentSummary(
            appointment_date=1,
            appointment_date=datetime(2024, 10, 15, 10, 0),
            patient_name="Faith Irakoze",
            doctor_name="Dr. Amina Mugisha",
            department="General Medicine",
            status="Completed",
            notes="Regular checkup"
        ),
        AppointmentSummary(
            appointment_id=2,
            appointment_date=datetime(2024, 10, 16, 14, 30),
            patient_name="Karangwa Arnold",
            doctor_name="Dr. Alex Kagame",
            department="Cardiology",
            status="Completed",
            notes="Follow-up on heart condition"
        ),
        AppointmentSummary(
            appointment_id=3,
            appointment_date=datetime(2024, 10, 18, 9, 0),
            patient_name="Alice Teta",
            doctor_name="Dr. Micheal Chen",
            department="Pediatrics",
            status="Cancelled",
            notes="Patient cancelled due to emergency"
        ),
        AppointmentSummary(
            appointment_id=4,
            appointment_date=datetime(2024, 11, 20, 11, 0),
            patient_name="Faith Irakoze",
            doctor_name="Dr. Amina Mugisha",
            department="General Medicine",
            status="no-show",
            notes=None
        )
    ]

    completed = sum(1 for a in dummy_appointments if a.status == "completed")
    cancelled = sum(1 for a in dummy_appointments if a.status == "cancelled")
    scheduled = sum(1 for a in dummy_appointments if a.status == "scheduled")
    no_show = sum(1 for a in dummy_appointments if a.status == "no-show")

    return AppointmentReportResponse(
        generated_at=datetime.now(),
        period=f"{request.start_date} to {request.end_date}",
        total_appointments=len(dummy_appointments),
        completed=completed,
        cancelled=cancelled,
        scheduled=scheduled,
        no_show=no_show,
        appointments=dummy_appointments
    )