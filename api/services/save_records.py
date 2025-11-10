#!/usr/bin/env python3

from fastapi import HTTPException, Depends
from data.hospital_model import Patient, MedicalRecords, Prescriptions, LabTests
from data.database import SessionLocal
from schemas.medical_record import MedicalRecor as medical_record
from schemas.medical_record import PrescriptionInfo as prescription
from schemas.medical_record import LabTestInfo as lab_test
from auth.dependencies import get_current_hospital                                
from services.search_user import search_user

class Record:
    """Base Class for handling medical records"""

    def __init__(self):
        pass

    def search_patient(self, patient_name:str)->list:
        """Search for patients by name"""
        with SessionLocal() as session:
            patients = search_user(
                user_name=patient_name,
                database=Patient,
                session=session
            )
        return patients or []
    
    def save_consultation(self, record: medical_record, patient_id:int, doctor_id:int=Depends())->str:
        """Save a new medical consultation record for a patient."""
        with SessionLocal() as session:
            patients = session.get(Patient, patient_id)
        if not patients:
            raise HTTPException(status_code=404, detail="Patient not found.")
        
        new_record = MedicalRecords(
            patient_id=patient_id,
            doctor_id=
        )