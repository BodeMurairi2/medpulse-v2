from sqlalchemy.orm import Session, joinedload
from data.models import Patient, Consultation, Prescription, LabTest, Appointment, Staff, Department

def get_patient_records_by_email(db: Session, email: str):
    patient = (
        db.query(Patient)
        .options(
            joinedload(Patient.consultations)
                .joinedload(Consultation.doctor)
                .joinedload(Staff.department),
            joinedload(Patient.prescriptions)
                .joinedload(Prescription.doctor)
                .joinedload(Staff.department),
            joinedload(Patient.lab_tests),
            joinedload(Patient.appointments)
                .joinedload(Appointment.doctor)
                .joinedload(Staff.department)
        )
        .filter(Patient.email == email)
        .first()
    )

    if not patient:
        return None

    return {
        "id": patient.id,
        "full_name": patient.full_name,
        "date_of_birth": patient.date_of_birth,
        "gender": patient.gender,
        "contact": patient.contact,
        "email": patient.email,
        "consultations": [
            {
                "doctor_name": c.doctor.full_name if c.doctor else None,
                "department_name": (
                    c.doctor.department.name if c.doctor and c.doctor.department else None
                ),
                "date": c.date,
                "notes": c.notes,
            }
            for c in patient.consultations
        ],
        "prescriptions": [
            {
                "medication": p.medication,
                "dosage": p.dosage,
                "duration": p.duration,
                "date_issued": p.date_issued,
            }
            for p in patient.prescriptions
        ],
        "lab_tests": [
            {
                "test_name": l.test_name,
                "result": l.result,
                "reference_range": l.reference_range,
                "date_conducted": l.date_conducted,
            }
            for l in patient.lab_tests
        ],
        "appointments": [
            {
                "doctor_name": a.doctor.full_name if a.doctor else None,
                "department_name": (
                    a.department.name if a.department else None
                ),
                "appointment_date": a.appointment_date,
                "status": a.status,
                "notes": a.notes,
            }
            for a in patient.appointments
        ],
    }
