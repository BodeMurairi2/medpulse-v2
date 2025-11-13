from sqlalchemy.orm import Session
from sqlalchemy import func
from schemas.reports import (
    PatientReportRequest, PatientReportResponse, PatientSummary,
    DoctorReportRequest, DoctorReportResponse, DoctorSummary,
    AppointmentReportRequest, AppointmentReportResponse, AppointmentSummary
)
from data.models import Patient, Staff, Appointment, Department
from datetime import datetime

def generate_patient_report(request: PatientReportRequest, db: Session) -> PatientReportResponse:
    """Generate report of patients registered/visited in the given period"""

    # Query patients created in the date range
    patients_query = db.query(Patient).filter(
        func.date(Patient.created_at) >= request.start_date,
        func.date(Patient.created_at) <= request.end_date
    )

    patients = patients_query.all()

    # Build patient summaries
    patient_summaries = []
    for patient in patients:
        # Get last visit date
        last_appointment = db.query(Appointment).filter(
            Appointment.patient_id == patient.id,
            Appointment.status == "completed"
        ).order_by(Appointment.appointment_date.desc()).first()

        # Count total visits
        total_visits = db.query(Appointment).filter(
            Appointment.patient_id == patient.id,
            Appointment.status == "completed"
        ).count()

        # Calculate age
        today = datetime.now().date()
        age = today.year - patient.date_of_birth.year - (
            (today.month, today.day) < (patient.date_of_birth.month, patient.date_of_birth.day)
        )

        patient_summaries.append(PatientSummary(
            patient_id=patient.id,
            first_name=patient.first_name,
            second_name=patient.second_name,
            age=age,
            gender=patient.gender,
            contact=patient.contact,
            last_visit=last_appointment.appointment_date.date() if last_appointment else None,
            total_visits=total_visits
        ))

    # Count new patients (those created in this period)
    new_patients_count = len(patients)

    return PatientReportResponse(
        generated_at=datetime.now(),
        period=f"{request.start_date} to {request.end_date}",
        total_patients=len(patient_summaries),
        new_patients=new_patients_count,
        patients=patient_summaries
    )

def generate_doctor_report(request: DoctorReportRequest, db: Session) -> DoctorReportResponse:
    """Generate performance report for doctors in the given period"""

    # Use request dates directly
    start_date = request.start_date
    end_date = request.end_date

    # Query doctors
    doctors_query = db.query(Staff).filter(Staff.role == "Doctor")

    if request.department:
        # Join with department to filter by name
        doctors_query = doctors_query.join(Department).filter(
            Department.name == request.department
        )

    doctors = doctors_query.all()

    # Build doctor summaries
    doctor_summaries = []
    for doctor in doctors:
        # Get department name
        department = db.query(Department).filter(
            Department.id == doctor.department_id
        ).first()

        # Count appointments in date range
        appointments = db.query(Appointment).filter(
            Appointment.doctor_id == doctor.id,
            func.date(Appointment.appointment_date) >= start_date,
            func.date(Appointment.appointment_date) <= end_date
        ).all()

        total_appointments = len(appointments)
        completed = sum(1 for a in appointments if a.status == "completed")
        cancelled = sum(1 for a in appointments if a.status == "cancelled")

        # Count unique patients seen
        unique_patients = db.query(Appointment.patient_id).filter(
            Appointment.doctor_id == doctor.id,
            Appointment.status == "completed",
            func.date(Appointment.appointment_date) >= start_date,
            func.date(Appointment.appointment_date) <= end_date
        ).distinct().count()

        doctor_summaries.append(DoctorSummary(
            doctor_id=doctor.id,
            full_name=doctor.full_name,
            specialization=doctor.specialization or "General",
            department=department.name if department else "Unassigned",
            total_appointments=total_appointments,
            completed_appointments=completed,
            cancelled_appointments=cancelled,
            total_patients_seen=unique_patients
        ))

    return DoctorReportResponse(
        generated_at=datetime.now(),
        period=f"{start_date} to {end_date}",
        total_doctors=len(doctor_summaries),
        doctors=doctor_summaries
    )

def generate_appointment_report(request: AppointmentReportRequest, db: Session) -> AppointmentReportResponse:
    """Generate report of appointments in the given period"""

    # Query appointments in date range
    appointments_query = db.query(Appointment).filter(
        func.date(Appointment.appointment_date) >= request.start_date,
        func.date(Appointment.appointment_date) <= request.end_date
    )

    # Filter by status if provided
    if request.status:
        appointments_query = appointments_query.filter(Appointment.status == request.status)

    # Filter by department if provided
    if request.department:
        appointments_query = appointments_query.join(Department).filter(
            Department.name == request.department
        )

    appointments = appointments_query.all()

    # Build appointment summaries
    appointment_summaries = []
    for appointment in appointments:
        # Get related data
        patient = db.query(Patient).filter(Patient.patient_id == appointment.patient_id).first()
        doctor = db.query(Staff).filter(Staff.id == appointment.doctor_id).first()
        department = db.query(Department).filter(Department.id == appointment.department_id).first()

        appointment_summaries.append(AppointmentSummary(
            appointment_id=appointment.id,
            appointment_date=appointment.appointment_date,
            patient_name=patient.full_name if patient else "Unknown",
            doctor_name=doctor.full_name if doctor else "Unknown",
            department=department.name if department else "Unknown",
            status=appointment.status,
            notes=appointment.notes
        ))

    # Calculate statistics
    completed = sum(1 for a in appointments if a.status == "completed")
    cancelled = sum(1 for a in appointments if a.status == "cancelled")
    scheduled = sum(1 for a in appointments if a.status == "scheduled")
    no_show = sum(1 for a in appointments if a.status == "no-show")

    return AppointmentReportResponse(
        generated_at=datetime.now(),
        period=f"{request.start_date} to {request.end_date}",
        total_appointments=len(appointments),
        completed=completed,
        cancelled=cancelled,
        scheduled=scheduled,
        no_show=no_show,
        appointments=appointment_summaries
    )