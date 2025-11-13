from fastapi import APIRouter, HTTPException, Depends, Header, status
from sqlalchemy.orm import Session
from data.database import get_db
from data.hospital_model import Patient
from schemas.patient import PatientCreate, PatientLogin, PatientOut, ChangePasswordSchema
from services.harsh import hash_password, verify_password
from services.jwt import create_access_token, decode_access_token
from services.token_blacklist import is_token_blacklisted, add_to_blacklist
from auth.dependencies import get_current_hospital
from datetime import datetime

router = APIRouter(prefix="/patients_portal_auth", tags=["Patients Authentication"])

@router.post("/login")
def patient_login(data : PatientLogin, db : Session = Depends(get_db)):
    patient = db.query(Patient).filter(Patient.email == data.email).first()
    if not patient or not verify_password(data.password, patient.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email or password")
    token = create_access_token({"patient_id": patient.patient_id})
    return {"access token": token, "token type": "bearer", "patient_id": patient.patient_id}   

@router.post("/change-password")
def change_password(
    payload : ChangePasswordSchema,
    authorization : str = Header(...),
    db : Session = Depends(get_db)
):
    if not authorization or " " not in authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    scheme, token = authorization.split(" ", 1)
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Authorization scheme must be Bearer")
    payload_token = decode_access_token(token)
    if payload_token is None:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    patient_id = payload_token.get("patient_id")
    if not patient_id:
        raise HTTPException(status_code=401, detail="Token does not contain patient_id")
    patient = db.query(Patient).get(patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    if not verify_password(payload.old_password, patient.password_hash):
        raise HTTPException(status_code=401, detail="Old password is incorrect")
    patient.password_hash = hash_password(payload.new_password)
    db.add(patient)
    db.commit()
    db.refresh(patient)

    return {"message": "Password changed successfuly"}


@router.post("/logout")
def patient_logout(authorization : str = Header(...)):
    if not authorization or " " not in authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing or invalid")
    scheme, token = authorization.split(" ", 1)
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=401, detail="Authorization must start with Bearer")
    add_to_blacklist(token)
    return {"message": "Logged out successfully"}