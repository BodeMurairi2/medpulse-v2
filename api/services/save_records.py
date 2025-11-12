#!/usr/bin/env python3

from datetime import date
from fastapi import HTTPException, status
from data.hospital_model import Patient, Doctor, MedicalRecord, Prescription, LabTestResult, Hospital
from data.database import SessionLocal
from services.search_patient import search_user
from schemas.medical_record import MedicalRecord as medical_record_schema
from schemas.medical_record import PrescriptionInfo as prescription_schema
from schemas.medical_record import LabTestInfo as lab_test_schema

class Record:
    """Base Class for handling medical records"""

    def __init__(self):
        pass

    def get_patients(self, doctor_id: int):
        """Return patients matching a doctor id"""
        with SessionLocal() as db:
            patient_ids = db.query(MedicalRecord.patient_id).filter(MedicalRecord.doctor_id == doctor_id).distinct()
            patients = db.query(Patient).filter(Patient.patient_id.in_(patient_ids)).all()
        return patients or []

    def search_patient(self, patient_name: str) -> list:
        """Search for patients by name"""
        with SessionLocal() as session:
            patients = search_user(
                user_name=patient_name,
                database=Patient,
                session=session
            )
        return patients or []

    def save_consultation(self, record: medical_record_schema, patient_id: int, doctor_id: int) -> str:
        """Save a new medical consultation record for a patient."""
        with SessionLocal() as session:
            patient = session.get(Patient, patient_id)
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found.")

            # get hospital name from doctor_id and lookup into hospital table
            hospital_id = session.query(Doctor).filter(Doctor.doctor_id == doctor_id).first().hospital_id
            hospital_name = session.query(Hospital).filter(Hospital.hospital_id == hospital_id).first().hospital_name
            
            new_record = MedicalRecord(
                patient_id=patient_id,
                doctor_id=doctor_id,
                diagnosis=record.diagnosis,
                treatment=record.treatment,
                notes=record.notes,
                hospital_id=hospital_id,
                hospital_name=hospital_name,
                created_by=record.created_by,
                follow_up_date=record.follow_up_date if hasattr(record, "follow_up_date") else None,
                record_date=record.record_date if hasattr(record, "record_date") else None
            )

            session.add(new_record)
            session.commit()
            session.refresh(new_record)

        return "Medical consultation record saved successfully."

    def save_prescription(self, prescription_data: prescription_schema, patient_id: int, doctor_id: int) -> str:
        """Save a new prescription for a medical record"""
        with SessionLocal() as session:
            patient = session.get(Patient, patient_id)
            if not patient:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")

            # take the latest medical record for the patient
            record = session.query(MedicalRecord).filter(
                MedicalRecord.patient_id == patient_id
            ).order_by(MedicalRecord.record_date.desc(), MedicalRecord.record_id.desc()).first()
            
            # find hospital name
            hospital_id = record.hospital_id
            hospital_name = session.query(Hospital).filter(Hospital.hospital_id == hospital_id).first().hospital_name

            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found for the patient.")
            
            new_prescription = Prescription(
                patient_id=patient_id,
                doctor_id=doctor_id,
                record_id=record.record_id,
                hospital_id=hospital_id,
                hospital_name=hospital_name,
                medicine_name=prescription_data.medicine_name,
                frequency=prescription_data.frequency,
                duration=prescription_data.duration,
                dosage=prescription_data.dosage,
                notes=prescription_data.notes,
                prescribed_by=prescription_data.prescribed_by,
                prescription_date=prescription_data.prescription_date or date.today(),
                prescription_details=prescription_data.prescription_details or None
            )

            session.add(new_prescription)
            session.commit()
            session.refresh(new_prescription)

        return "Prescription saved successfully."

    def save_lab_test(self, lab_test_data: lab_test_schema, record_id: int, patient_id: int, doctor_id: int) -> str:
        """Save a new lab test result for a medical record"""
        with SessionLocal() as session:
            patient = session.get(Patient, patient_id)
            if not patient:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")

            new_lab_test = LabTestResult(
                patient_id=patient_id,
                doctor_id=doctor_id,
                record_id=record_id,
                test_name=lab_test_data.test_name,
                result_value=lab_test_data.result_value,
                result_date=lab_test_data.result_date,
                notes=lab_test_data.notes,
                attached_files=lab_test_data.attached_files
            )

            session.add(new_lab_test)
            session.commit()
            session.refresh(new_lab_test)

        return "Lab test result saved successfully."
