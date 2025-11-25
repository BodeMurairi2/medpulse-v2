#!/usr/bin/env python3

import base64
from io import BytesIO
import os
import uuid
import qrcode

from fastapi import APIRouter, HTTPException, Depends, Header, status
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse, JSONResponse
import qrcode

from data.database import get_db, SessionLocal
from data.hospital_model import Patient, MedicalRecord, Prescription, LabTestResult
from schemas.patient import PatientLogin, ChangePasswordSchema
from schemas.medical_record import PatientRecordsOut

from services.harsh import hash_password, verify_password
from services.jwt import create_access_token, decode_access_token
from services.token_blacklist import is_token_blacklisted, add_to_blacklist
from services.patient_service import get_patient_records_by_id

router = APIRouter(prefix="/patients_portal_auth", tags=["Patients Authentication"])

# JWT validation
def get_current_patient(authorization: str = Header(...)):
    if not authorization or " " not in authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    
    scheme, token = authorization.split(" ", 1)
    
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Authorization must start with Bearer")
    
    if is_token_blacklisted(token):
        raise HTTPException(status_code=401, detail="Token has been revoked")
    
    payload = decode_access_token(token)
    if not payload or "patient_id" not in payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    return payload["patient_id"]

# LOGIN
@router.post("/login")
def patient_login(data: PatientLogin, db: Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.email == data.email).first()
    if not patient or not verify_password(data.password, patient.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    
    token = create_access_token({"patient_id": patient.patient_id})
    return {
        "access_token": token,
        "token_type": "bearer",
        "patient_id": patient.patient_id
    }


# CHANGE PASSWORD
@router.post("/change-password")
def change_password(
    payload: ChangePasswordSchema,
    current_patient_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    patient = db.query(Patient).get(current_patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    if not verify_password(payload.old_password, patient.password_hash):
        raise HTTPException(status_code=401, detail="Old password is incorrect")
    
    patient.password_hash = hash_password(payload.new_password)
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return {"message": "Password changed successfully"}


# LOGOUT
@router.post("/logout")
def patient_logout(current_patient_id: int = Depends(get_current_patient), authorization: str = Header(...)):
    scheme, token = authorization.split(" ", 1)
    add_to_blacklist(token)
    return {"message": "Logged out successfully"}

# GET patient general info
@router.get("/general_info")
def get_patient_info(
    current_patient_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    """Get current patient info"""
    patient = db.query(Patient).filter(Patient.patient_id == current_patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return {
        "patient_id": patient.patient_id,
        "patient_name": f"{patient.first_name} {patient.second_name}"
    }

# GET PATIENT RECORDS
@router.get("/patients/{patient_id}/records", response_model=PatientRecordsOut)
def get_patient_records(
    patient_id: int,
    current_patient_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    if patient_id != current_patient_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this patient's records")
    
    patient_records = get_patient_records_by_id(db, patient_id)
    if not patient_records:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    return patient_records

# GENERATE QR
@router.get("/{patient_id}/generate-qr")
def generate_qr(patient_id: int):
    """
    Generate a QR code that links to the patient's medical records
    and return patient info + medical history as JSON.
    """
    db = SessionLocal()

    # Fetch the patient
    patient = db.query(Patient).filter(Patient.patient_id == patient_id).first()
    if not patient:
        return {"error": "Patient not found"}

    # Fetch medical records
    medical_records = db.query(MedicalRecord).filter(
        MedicalRecord.patient_id == patient_id
    ).all()

    # Fetch prescriptions
    prescriptions = db.query(Prescription).filter(
        Prescription.patient_id == patient_id
    ).all()

    # Fetch lab tests
    lab_tests = db.query(LabTestResult).filter(
        LabTestResult.patient_id == patient_id
    ).all()

    # Generate token
    token = str(uuid.uuid4())

    # URL to access the records
    share_url = f"http://localhost:8080/patients/{patient_id}/records?token={token}"

    # Generate the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(share_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR code to folder
    os.makedirs("qrcodes", exist_ok=True)
    qr_filename = f"patient_{patient_id}_qr.png"
    qr_path = f"qrcodes/{qr_filename}"
    img.save(qr_path)

    # URL for frontend to access the QR code
    qr_url = f"http://localhost:8080/qrcodes/{qr_filename}"

    # Build response JSON
    response = {
        "id": patient.patient_id,
        "first_name": patient.first_name,
        "second_name": patient.second_name,
        "date_of_birth": str(patient.date_of_birth),
        "gender": patient.gender,
        "contact": patient.phone_number,
        "email": patient.email,
        "qr_code_url": qr_url,
        "records_access_url": share_url,
        "medical_records": [
            {
                "patient_id": r.patient_id,
                "doctor_id": r.doctor_id,
                "hospital_id": r.hospital_id,
                "hospital_name": r.hospital_name,
                "diagnosis": r.diagnosis,
                "treatment": r.treatment,
                "notes": r.notes,
                "follow_up_date": r.follow_up_date,
                "created_by": r.created_by,
                "record_date": str(r.record_date),
                "created_at": r.created_at,
                "updated_at": r.updated_at,
            }
            for r in medical_records
        ],
        "prescriptions": [
            {
                "patient_id": p.patient_id,
                "doctor_id": p.doctor_id,
                "record_id": p.record_id,
                "hospital_id": p.hospital_id,
                "hospital_name": p.hospital_name,
                "medicine_name": p.medicine_name,
                "frequency": p.frequency,
                "duration": p.duration,
                "notes": p.notes,
                "dosage": p.dosage,
                "prescription_details": p.prescription_details,
                "prescribed_by": p.prescribed_by,
                "prescription_date": str(p.prescription_date),
                "created_at": p.created_at,
                "updated_at": p.updated_at,
            }
            for p in prescriptions
        ],
        "lab_tests": [
            {
                "patient_id": l.patient_id,
                "doctor_id": l.doctor_id,
                "record_id": l.record_id,
                "hospital_id": l.hospital_id,
                "hospital_name": l.hospital_name,
                "test_name": l.test_name,
                "result_value": l.result_value,
                "result_date": str(l.result_date),
                "notes": l.notes,
                "doctor_name": l.doctor_name,
                "files": l.files or [],
                "created_at": l.created_at,
                "updated_at": l.updated_at,
            }
            for l in lab_tests
        ],
    }

    return response
