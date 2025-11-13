#!/usr/bin/env python3

from sqlalchemy.orm import Session, joinedload
from data.hospital_model import Hospital, Department, Doctor, Patient, MedicalRecord, LabTestResult, Prescription, LabTestFile

def get_patient_records_by_id(db: Session, patient_id: int):
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
                "doctor_name": f"{mr.doctor.first_name} {mr.doctor.last_name}" if mr.doctor else None,
                "hospital_name": mr.hospital_name or (mr.hospital.hospital_name if mr.hospital else None),
                "diagnosis": mr.diagnosis,
                "treatment": mr.treatment,
                "notes": mr.notes,
                "follow_up_date": mr.follow_up_date,
                "record_date": mr.record_date,
            }
            for mr in patient.medical_records
        ],
        "prescriptions": [
            {
                "medicine_name": p.medicine_name,
                "dosage": p.dosage,
                "frequency": p.frequency,
                "duration": p.duration,
                "notes": p.notes,
                "doctor_name": f"{p.doctor.first_name} {p.doctor.last_name}" if p.doctor else None,
                "record_id": p.record_id
            }
            for p in patient.prescriptions
        ],
        "lab_tests": [
            {
                "test_name": l.test_name,
                "result_value": l.result_value,
                "result_date": l.result_date,
                "notes": l.notes,
                "doctor_name": l.doctor_name,
                "files": [f.file_url for f in l.files]  # Lab test files URLs
            }
            for l in patient.lab_tests
        ]
    }
