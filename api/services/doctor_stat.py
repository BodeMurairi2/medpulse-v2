#!/usr/bin/env python3

from sqlalchemy import func
from data import MedicalRecord, PrescriptionManagement, LabTestResult, PatientRegistration

def get_doctor_stats(db_session, doctor_id):
    """ Function that returns stats related to a doctor activities
    at tbe hospital
    """
    # Count medical records linked to this doctor
    record_count = db_session.query(func.count(MedicalRecord.id))\
        .filter(MedicalRecord.doctor_id == doctor_id)\
        .scalar()

    # Count prescriptions issued by this doctor
    prescription_count = db_session.query(func.count(PrescriptionManagement.id))\
        .filter(PrescriptionManagement.doctor_id == doctor_id)\
        .scalar()

    lab_test_count = db_session.query(func.count(LabTestResult.id))\
        .filter(LabTestResult.doctor_id == doctor_id)\
        .scalar()

    return {
        "doctor_id": doctor_id,
        "medical_records": record_count,
        "prescriptions": prescription_count,
        "LabTestResult": lab_test_count
    }

def get_patients_by_doctor(db_session, doctor_id):
    """
    Return a reversed list of patients' names associated with a given doctor_id.
    The latest patient entries appear first.
    """
    patients = (
        db_session.query(PatientRegistration.first_name, PatientRegistration.last_name)
        .join(MedicalRecord, MedicalRecord.patient_id == PatientRegistration.id)
        .filter(MedicalRecord.doctor_id == doctor_id)
        .distinct()
        .all()
    )
    # all the names
    full_names = [f"{p.first_name} {p.last_name}" for p in patients]
    return full_names[::-1][:3]


if __name__ == "__main__":
    get_doctor_stats(db_session, doctor_id)
    get_patients_by_doctor(db_session, doctor_id)
