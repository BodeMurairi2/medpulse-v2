from fastapi import APIRouter, HTTPException, Depends, Header
from datetime import datetime
from sqlalchemy.orm import Session
from data.database import get_db
from data.hospital_model import Doctor, Patient
from schemas.patient import PatientCreate, PatientOut
from services.harsh import hash_password
from auth.dependencies import get_current_hospital

router = APIRouter(prefix="/patients_portal_create", tags=["Patients Create"])

@router.post("/create", response_model=PatientOut)
def create_patient(
    patient : PatientCreate,
    hospital_id : int = Depends(get_current_hospital),
    db : Session = Depends(get_db)
):
    if patient.email:
        existing = db.query(Patient).filter(Patient.email == patient.email).first()
        if existing:
            raise HTTPException(status_code=404, detail="Patient with this email already exists")
    hashed = hash_password(patient.password)
    new_patient = Patient(
    first_name=patient.first_name,
    second_name=patient.second_name,
    email=patient.email,
    phone_number=patient.phone_number,
    date_of_birth=patient.date_of_birth,
    password_hash=hashed,
    created_at=datetime.utcnow()
)
    db.add(new_patient)
    db.commit()
    db.refresh(new_patient)
    return new_patient
