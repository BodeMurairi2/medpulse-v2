#!/usr/bin/env python3

from sqlalchemy.orm import Session, joinedload
from data.hospital_model import (
    Hospital, Department, Doctor, Patient,
    MedicalRecord, LabTestResult, Prescription, LabTestFile
)

def get_patient_records_by_id(db: Session, patient_id: int):
    """
    Fetches all patient records including medical records, prescriptions, and lab tests,
    formatted to match the PatientRecordsOut Pydantic model.
    """
    patient = (
        db.query(Patient)
        .options(
            joinedload(Patient.medical_records)
                .joinedload(MedicalRecord.doctor)
                .joinedload(Doctor.hospital),
            joinedload(Patient.prescriptions)
                .joinedload(Prescription.doctor),
            joinedload(Patient.lab_tests)
                .joinedload(LabTestResult.files)
        )
        .filter(Patient.patient_id == patient_id)
        .first()
    )

    if not patient:
        return None

    return {
        "id": patient.patient_id,
        "full_name": f"{patient.first_name} {patient.middle_name or ''} {patient.second_name or ''}".strip(),
        "date_of_birth": patient.date_of_birth,
        "gender": patient.gender,
        "contact": patient.phone_number,
        "email": patient.email,
        "medical_records": [
            {
                "patient_id": mr.patient_id,
                "doctor_id": mr.doctor_id,
                "hospital_id": mr.hospital_id,
                "created_by": f"{mr.doctor.first_name} {mr.doctor.last_name}" if mr.doctor else None,
                "hospital_name": mr.hospital_name or (mr.hospital.hospital_name if mr.hospital else None),
                "diagnosis": mr.diagnosis,
                "treatment": mr.treatment,
                "notes": mr.notes,
                "follow_up_date": mr.follow_up_date,
                "record_date": mr.record_date,
                "created_at": mr.created_at,
                "updated_at": mr.updated_at
            }
            for mr in patient.medical_records
        ],
        "prescriptions": [
            {
                "patient_id": p.patient_id,
                "doctor_id": p.doctor_id,
                "record_id": p.record_id,
                "hospital_id": p.hospital_id,
                "prescribed_by": f"{p.doctor.first_name} {p.doctor.last_name}" if p.doctor else None,
                "hospital_name": p.hospital_name,
                "medicine_name": p.medicine_name,
                "dosage": p.dosage,
                "frequency": p.frequency,
                "duration": p.duration,
                "notes": p.notes,
                "prescription_details": p.prescription_details,
                "prescription_date": p.prescription_date,
                "created_at": p.created_at,
                "updated_at": p.updated_at
            }
            for p in patient.prescriptions
        ],
        "lab_tests": [
            {
                "patient_id": l.patient_id,
                "doctor_id": l.doctor_id,
                "record_id": l.record_id,
                "hospital_id": l.hospital_id,
                "doctor_name": l.doctor_name,
                "hospital_name": l.hospital_name,
                "test_name": l.test_name,
                "result_value": l.result_value,
                "result_date": l.result_date,
                "notes": l.notes,
                "created_at": l.created_at,
                "updated_at": l.updated_at,
                "files": [f.file_url for f in l.files]  # Lab test files URLs
            }
            for l in patient.lab_tests
        ]
    }
