#!/usr/bin/env python3
from datetime import date
from fastapi import File, HTTPException, status, UploadFile
from pytest import Session
from data.hospital_model import Patient, Doctor, MedicalRecord, Prescription, LabTestResult, Hospital, LabTestFile
from data.database import SessionLocal
from services.search_patient import search_user
from services.upload import upload_user_document
from schemas.medical_record import MedicalRecord as medical_record_schema
from schemas.medical_record import PrescriptionInfo as prescription_schema
from schemas.medical_record import LabTestInfo as lab_test_schema

class Record:
    """Base Class for handling medical records"""

    def __init__(self):
        pass

    # ----------------------- GET / SEARCH -----------------------
    def get_patients(self, doctor_id: int):
        """Return patients matching a doctor id"""
        with SessionLocal() as db:
            patient_ids = db.query(MedicalRecord.patient_id).filter(MedicalRecord.doctor_id == doctor_id).distinct()
            patients = db.query(Patient).filter(Patient.patient_id.in_(patient_ids)).all()
        return patients or []

    def search_patient(self, patient_name) -> list:
        """Search for patients by name or id"""
        if isinstance(patient_name, int):
            with SessionLocal() as session:
                patient = session.query(Patient).filter(Patient.patient_id == patient_name).first()
                return [patient] if patient else []
        
        with SessionLocal() as session:
            patients = search_user(
                user_name=patient_name,
                database=Patient,
                session=session
            )
        return patients or []


    def get_doctors(self):
        """View all doctors per department"""
        with SessionLocal() as db:
            load_doctors = db.query(Doctor).all()

        if not load_doctors:
            raise HTTPException(status_code=400, detail="No doctors in the platform")

        doctors_list = {}
        for doc in load_doctors:
            dept_key = doc.department
            if dept_key not in doctors_list:
                doctors_list[dept_key] = []

            doctors_list[dept_key].append({
                "first_name": doc.first_name,
                "last_name": doc.last_name,
                "gender": doc.gender,
                "phone_number": doc.phone_number,
                "email": doc.email
            })
        return doctors_list

    def get_patient_medical_history(patient_id: int, db: Session):
        """Fetch all medical records (consultations, prescriptions, lab tests) for a patient."""
        
        # Fetch consultations
        consultations = db.query(MedicalRecord).filter(MedicalRecord.patient_id == patient_id).all()
        consultation_records = [
            {
                "date": c.record_date or date.today(),
                "type": "Consultation",
                "description": f"Diagnosis: {c.diagnosis}, Treatment: {c.treatment}, Notes: {c.notes or '-'}",
                "doctor": c.created_by
            }
            for c in consultations
        ]

        # Fetch prescriptions
        prescriptions = db.query(Prescription).filter(Prescription.patient_id == patient_id).all()
        prescription_records = [
            {
                "date": p.prescription_date or date.today(),
                "type": "Prescription",
                "description": f"Medicine: {p.medicine_name}, Dosage: {p.dosage}, Frequency: {p.frequency}, Duration: {p.duration}, Notes: {p.notes or '-'}",
                "doctor": p.prescribed_by
            }
            for p in prescriptions
        ]

        # Fetch lab tests
        lab_tests = db.query(LabTestResult).filter(LabTestResult.patient_id == patient_id).all()
        lab_test_records = [
            {
                "date": l.result_date or date.today(),
                "type": "Lab Test",
                "description": f"Test: {l.test_name}, Result: {l.result_value}, Notes: {l.notes or '-'}",
                "doctor": l.doctor_name
            }
            for l in lab_tests
        ]

        # Combine all records and sort by date descending
        all_records = consultation_records + prescription_records + lab_test_records
        all_records.sort(key=lambda x: x["date"], reverse=True)

        return all_records

    # ----------------------- SAVE -----------------------
    def save_consultation(self, record: medical_record_schema, patient_id: int, doctor_id: int) -> str:
        """Save a new medical consultation record for a patient."""
        with SessionLocal() as session:
            patient = session.get(Patient, patient_id)
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found.")

            doctor = session.get(Doctor, doctor_id)
            hospital = session.get(Hospital, doctor.hospital_id)

            # get doctor name from the doctor table
            doctor_name = session.get(Doctor, doctor_id).first_name + " " + session.get(Doctor, doctor_id).last_name

            new_record = MedicalRecord(
                patient_id=patient_id,
                doctor_id=doctor_id,
                diagnosis=record.diagnosis,
                treatment=record.treatment,
                notes=record.notes,
                hospital_id=doctor.hospital_id,
                hospital_name=hospital.hospital_name,
                created_by=doctor_name,
                follow_up_date=getattr(record, "follow_up_date", None),
                record_date=getattr(record, "record_date", None)
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

            record = session.query(MedicalRecord).filter(
                MedicalRecord.patient_id == patient_id
            ).order_by(MedicalRecord.record_date.desc(), MedicalRecord.record_id.desc()).first()

            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found for the patient.")

            hospital = session.get(Hospital, record.hospital_id)
            # get doctor name from the doctor table
            doctor_name = session.get(Doctor, doctor_id).first_name + " " + session.get(Doctor, doctor_id).last_name

            new_prescription = Prescription(
                patient_id=patient_id,
                doctor_id=doctor_id,
                record_id=record.record_id,
                hospital_id=record.hospital_id,
                hospital_name=hospital.hospital_name,
                medicine_name=prescription_data.medicine_name,
                frequency=prescription_data.frequency,
                duration=prescription_data.duration,
                dosage=prescription_data.dosage,
                notes=prescription_data.notes,
                prescribed_by=doctor_name,
                prescription_date=prescription_data.prescription_date or date.today(),
                prescription_details=prescription_data.prescription_details or None
            )
            session.add(new_prescription)
            session.commit()
            session.refresh(new_prescription)
        return "Prescription saved successfully."
    
    def save_lab_test(self, lab_test_data: lab_test_schema, patient_id: int, doctor_id: int) -> LabTestResult:
        """Save a new lab test result for a patient"""
        with SessionLocal() as session:
            patient = session.get(Patient, patient_id)
            if not patient:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found.")

            record = session.query(MedicalRecord).filter(
                MedicalRecord.patient_id == patient_id
            ).order_by(MedicalRecord.record_date.desc(), MedicalRecord.record_id.desc()).first()

            if not record:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Medical record not found for the patient.")

            hospital = session.get(Hospital, record.hospital_id)
            # get doctor name from the doctor table
            doctor_name = session.get(Doctor, doctor_id).first_name + " " + session.get(Doctor, doctor_id).last_name
            new_lab_test = LabTestResult(
                patient_id=patient_id,
                doctor_id=doctor_id,
                record_id=record.record_id,
                hospital_id=record.hospital_id,
                hospital_name=hospital.hospital_name,
                test_name=lab_test_data.test_name,
                result_value=lab_test_data.result_value,
                result_date=lab_test_data.result_date or date.today(),
                notes=lab_test_data.notes,
                doctor_name=doctor_name
            )
            session.add(new_lab_test)
            session.commit()
            session.refresh(new_lab_test)
            return new_lab_test

    def save_lab_test_file(self, lab_test_id: int, file: UploadFile) -> str:
        """Upload a file for a specific lab test result and save in LabTestFile table"""
        with SessionLocal() as session:
            lab_test = session.get(LabTestResult, lab_test_id)
            if not lab_test:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lab test not found")

            public_url = upload_user_document(
                file=file,
                hospital_name=lab_test.hospital_name,
                patient_name=f"{lab_test.patient.first_name} {lab_test.patient.second_name or ''}",
                report_type=lab_test.test_name
            )
            lab_test_file = LabTestFile(
                lab_test_id=lab_test_id,
                file_url=public_url
            )
            session.add(lab_test_file)
            session.commit()
            session.refresh(lab_test_file)
            return public_url

    # ----------------------- UPDATE -----------------------
    def update_consultation(self, record_id: int, updated_data: medical_record_schema) -> str:
        """Update an existing consultation"""
        with SessionLocal() as session:
            record = session.get(MedicalRecord, record_id)
            if not record:
                raise HTTPException(status_code=404, detail="Medical record not found.")
            record.diagnosis = updated_data.diagnosis
            record.treatment = updated_data.treatment
            record.notes = updated_data.notes
            record.follow_up_date = getattr(updated_data, "follow_up_date", record.follow_up_date)
            record.record_date = getattr(updated_data, "record_date", record.record_date)
            session.commit()
        return "Medical consultation updated successfully."

    def update_prescription(self, prescription_id: int, updated_data: prescription_schema) -> str:
        """Update an existing prescription"""
        with SessionLocal() as session:
            prescription = session.get(Prescription, prescription_id)
            if not prescription:
                raise HTTPException(status_code=404, detail="Prescription not found.")
            prescription.medicine_name = updated_data.medicine_name
            prescription.frequency = updated_data.frequency
            prescription.duration = updated_data.duration
            prescription.dosage = updated_data.dosage
            prescription.notes = updated_data.notes
            prescription.prescribed_by = updated_data.prescribed_by
            prescription.prescription_date = updated_data.prescription_date or prescription.prescription_date
            prescription.prescription_details = updated_data.prescription_details or prescription.prescription_details
            session.commit()
        return "Prescription updated successfully."

    def update_lab_test(self, lab_test_id: int, updated_data: lab_test_schema) -> str:
        """Update an existing lab test result"""
        with SessionLocal() as session:
            lab_test = session.get(LabTestResult, lab_test_id)
            if not lab_test:
                raise HTTPException(status_code=404, detail="Lab test not found.")
            lab_test.test_name = updated_data.test_name
            lab_test.result_value = updated_data.result_value
            lab_test.result_date = updated_data.result_date or lab_test.result_date
            lab_test.notes = updated_data.notes
            lab_test.doctor_name = updated_data.doctor_name
            session.commit()
        return "Lab test result updated successfully."

    def update_lab_test_file(self, lab_test_file_id: int, new_file: UploadFile) -> str:
        """Update an existing lab test file"""
        with SessionLocal() as session:
            lab_test_file = session.get(LabTestFile, lab_test_file_id)
            if not lab_test_file:
                raise HTTPException(status_code=404, detail="Lab test file not found.")
            
            lab_test = session.get(LabTestResult, lab_test_file.lab_test_id)
            public_url = upload_user_document(
                file=new_file,
                hospital_name=lab_test.hospital_name,
                patient_name=f"{lab_test.patient.first_name} {lab_test.patient.second_name or ''}",
                report_type=lab_test.test_name
            )
            lab_test_file.file_url = public_url
            session.commit()
        return public_url
