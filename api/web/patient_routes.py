#!/usr/bin/env python3

from fastapi import APIRouter, HTTPException, Depends, Header, status
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
import qrcode
import json
import base64
from io import BytesIO
from cryptography.fernet import Fernet

from data.database import get_db
from data.hospital_model import Patient
from schemas.patient import PatientLogin, ChangePasswordSchema
from schemas.medical_record import PatientRecordsOut

from services.harsh import hash_password, verify_password
from services.jwt import create_access_token, decode_access_token
from services.token_blacklist import is_token_blacklisted, add_to_blacklist
from services.patient_service import get_patient_records_by_id

router = APIRouter(prefix="/patients_portal_auth", tags=["Patients Authentication"])

# CONFIG: Fernet Encryption Key
FERNET_KEY = Fernet.generate_key()
fernet = Fernet(FERNET_KEY)


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


# Generate QR code with encrypted patient data
def generate_patient_qr(first_name, second_name, email, phone):
    data = {
        "first_name": first_name,
        "second_name": second_name,
        "email": email,
        "phone": phone
    }

    # Convert to JSON bytes and encrypt
    json_bytes = json.dumps(data).encode()
    encrypted_bytes = fernet.encrypt(json_bytes)
    qr_content = encrypted_bytes.decode()

    # Generate smaller QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_Q,
        box_size=6,   # smaller than default 10
        border=3,     # smaller border
    )
    qr.add_data(qr_content)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)

    base64_qr = base64.b64encode(buffer.read()).decode("utf-8")
    return base64_qr


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


# GET ENCRYPTED QR CODE
@router.get("/patients/{patient_id}/qrcode")
def get_patient_qrcode(
    patient_id: int,
    current_patient_id: int = Depends(get_current_patient),
    db: Session = Depends(get_db)
):
    if patient_id != current_patient_id:
        raise HTTPException(status_code=403, detail="Not authorized to access this patient's QR code")

    patient = db.query(Patient).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    qr_base64 = generate_patient_qr(
        first_name=patient.first_name,
        second_name=patient.second_name,
        email=patient.email,
        phone=patient.phone_number
    )

    return JSONResponse({
        "qr_code_base64": qr_base64,
        "message": "Encrypted QR code generated successfully"
    })
