#!/usr/bin/env python3
from fastapi import APIRouter, HTTPException, Depends, Header, status, Body, UploadFile, File
from sqlalchemy.orm import Session
from data.database import get_db
from data.hospital_model import Doctor
from schemas.doctor import DoctorLogin, ChangePassword as ChangePasswordSchema
from schemas.medical_record import MedicalRecord as medical_record_schema
from schemas.medical_record import PrescriptionInfo as prescription_schema
from schemas.medical_record import LabTestInfo as lab_test_schema
from services.harsh import verify_password, hash_password
from services.jwt import create_access_token, decode_access_token
from services.token_blacklist import add_to_blacklist
from services.save_records import Record
from auth.doctor_dependencies import get_current_doctor

doctor_portal_router = APIRouter(
    prefix="/doctor_portal",
    tags=["Doctor Portal"]
)

record = Record()

# ----------------------- AUTH -----------------------
@doctor_portal_router.post("/login")
def login_doctor(doctor_login: DoctorLogin, db: Session = Depends(get_db)):
    doctor = db.query(Doctor).filter(Doctor.email == doctor_login.email).first()
    if not doctor or not verify_password(doctor_login.password, doctor.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid doctor email or password")
    access_token = create_access_token({"doctor_id": doctor.doctor_id})
    return {"access_token": access_token, "token_type": "bearer", "doctor_id": doctor.doctor_id}

@doctor_portal_router.post("/logout")
def logout(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization header")
    token = authorization.split(" ")[1]
    add_to_blacklist(token)
    return {"message": "Logged out successfully"}

@doctor_portal_router.post("/change_password")
def change_password(
    payload: ChangePasswordSchema,
    authorization: str = Header(...),
    db: Session = Depends(get_db),
    doctor_id: int = Depends(get_current_doctor)
):
    if not authorization or " " not in authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing or invalid")
    scheme, token = authorization.split(" ", 1)
    if scheme.lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization scheme must be Bearer")
    payload_token = decode_access_token(token)
    if payload_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")

    doctor_id = payload_token.get("doctor_id")
    doctor = db.query(Doctor).get(doctor_id)
    if not doctor:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Doctor not found")
    if not verify_password(payload.old_password, doctor.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Old password is incorrect")
    
    doctor.password_hash = hash_password(payload.new_password)
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return {"message": "Password changed successfully"}

# ----------------------- PATIENTS -----------------------
@doctor_portal_router.get("/patients")
def get_patients(doctor_id: int = Depends(get_current_doctor)):
    return record.get_patients(doctor_id=doctor_id)

@doctor_portal_router.get("/patients/search/{patient_name}")
def get_patient(patient_name: str, _: int = Depends(get_current_doctor)):
    return record.search_patient(patient_name=patient_name)

@doctor_portal_router.get("/doctors/all")
def get_all_doctors( _: int = Depends(get_current_doctor)):
    return record.get_doctors()

"""
@doctor_portal_router.get("/patients/{patient_id}/records")
def get_records(
    patient_id: int,
    doctor_id: int = Depends(get_current_doctor)
):
    return record.get_patient_medical_history(patient_id=patient_id, doctor_id=doctor_id)
"""
# ----------------------- CREATE -----------------------
@doctor_portal_router.post("/patients/new_consultation/{patient_id}")
def create_new_consultation(
    patient_id: int,
    consultation: medical_record_schema = Body(...),
    doctor_id: int = Depends(get_current_doctor)
):
    return record.save_consultation(record=consultation, patient_id=patient_id, doctor_id=doctor_id)

@doctor_portal_router.post("/patients/new_prescription/{patient_id}")
def create_new_prescription(
    patient_id: int,
    prescription: prescription_schema = Body(...),
    doctor_id: int = Depends(get_current_doctor)
):
    return record.save_prescription(prescription_data=prescription, patient_id=patient_id, doctor_id=doctor_id)

@doctor_portal_router.post("/patients/new_lab_test/{patient_id}")
def create_new_lab_test(
    patient_id: int,
    lab_test: lab_test_schema = Body(...),
    doctor_id: int = Depends(get_current_doctor)
):
    return record.save_lab_test(lab_test_data=lab_test, patient_id=patient_id, doctor_id=doctor_id)

@doctor_portal_router.post("/patients/lab_test/{lab_test_id}/upload_file")
def upload_lab_test_file(
    lab_test_id: int,
    file: UploadFile = File(...),
    doctor_id: int = Depends(get_current_doctor)
):
    return record.save_lab_test_file(lab_test_id=lab_test_id, file=file)

# ----------------------- UPDATE -----------------------
@doctor_portal_router.put("/patients/update_consultation/{record_id}")
def update_consultation(
    record_id: int,
    updated_consultation: medical_record_schema = Body(...),
    doctor_id: int = Depends(get_current_doctor)
):
    return record.update_consultation(record_id=record_id, updated_data=updated_consultation)

@doctor_portal_router.put("/patients/update_prescription/{prescription_id}")
def update_prescription(
    prescription_id: int,
    updated_prescription: prescription_schema = Body(...),
    doctor_id: int = Depends(get_current_doctor)
):
    return record.update_prescription(prescription_id=prescription_id, updated_data=updated_prescription)

@doctor_portal_router.put("/patients/update_lab_test/{lab_test_id}")
def update_lab_test(
    lab_test_id: int,
    updated_lab_test: lab_test_schema = Body(...),
    doctor_id: int = Depends(get_current_doctor)
):
    return record.update_lab_test(lab_test_id=lab_test_id, updated_data=updated_lab_test)

@doctor_portal_router.put("/patients/update_lab_test_file/{lab_test_file_id}")
def update_lab_test_file(
    lab_test_file_id: int,
    new_file: UploadFile = File(...),
    doctor_id: int = Depends(get_current_doctor)
):
    return record.update_lab_test_file(lab_test_file_id=lab_test_file_id, new_file=new_file)
