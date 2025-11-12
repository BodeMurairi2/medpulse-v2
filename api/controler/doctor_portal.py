#!/usr/bin/env python3

from fastapi import APIRouter, HTTPException, Depends, Header, status, Body
from sqlalchemy.orm import Session
from data.database import get_db
from data.hospital_model import Doctor
from schemas.doctor import DoctorLogin
from schemas.medical_record import MedicalRecord as medical_record_schema
from schemas.medical_record import PrescriptionInfo as prescription_schema
from schemas.medical_record import LabTestInfo as lab_test_schema
from services.harsh import verify_password
from services.jwt import create_access_token
from services.token_blacklist import add_to_blacklist
from services.save_records import Record
from auth.doctor_dependencies import get_current_doctor

doctor_portal_router = APIRouter(
    prefix="/doctor_portal",
    tags=["Doctor Portal"]
)

record = Record()

@doctor_portal_router.post("/login")
def login_doctor(doctor_login: DoctorLogin, db: Session = Depends(get_db)):
    """
    Authenticate a doctor and return a JWT token.
    """
    # Query doctor by email
    doctor = db.query(Doctor).filter(Doctor.email == doctor_login.email).first()

    # Verify password
    if not doctor or not verify_password(doctor_login.password, doctor.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid doctor email or password"
        )

    # Create JWT token
    access_token = create_access_token({"doctor_id": doctor.doctor_id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "doctor_id": doctor.doctor_id
    }

@doctor_portal_router.post("/logout")
def logout(authorization: str = Header(...)):
    """
    Logout a doctor by blacklisting their JWT token.
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization header")

    token = authorization.split(" ")[1]
    add_to_blacklist(token)

    return {"message": "Logged out successfully"}

@doctor_portal_router.get("/patients")
def get_patients(doctor_id: int = Depends(get_current_doctor), db: Session = Depends(get_db)):
    """
    Retrieve a list of patients assigned to the logged-in doctor.
    """

    return record.get_patients(doctor_id= doctor_id)

@doctor_portal_router.get("/patients/search/{patient_name}")
def get_patient(patient_name: str, _: int = Depends(get_current_doctor), db: Session = Depends(get_db)):
    """Retrieve a list of patients matching the name"""
    return record.search_patient(patient_name=patient_name)

@doctor_portal_router.post("/patients/new_consultation/{patient_id}")
def create_new_consultation(patient_id:int, 
                            consultation: medical_record_schema = Body(...),
                            doctor_id: int = Depends(get_current_doctor)
                            ):
    """Create a new consultation"""
    return record.save_consultation(record = consultation, patient_id=patient_id, doctor_id=doctor_id)

@doctor_portal_router.post("/patients/new_prescription/{patient_id}")
def create_new_prescription(patient_id:int, 
                            prescription: prescription_schema = Body(...),
                            doctor_id: int = Depends(get_current_doctor)
                            ):
    """Create a new prescription"""
    return record.save_prescription(prescription_data = prescription, patient_id=patient_id, doctor_id=doctor_id)
