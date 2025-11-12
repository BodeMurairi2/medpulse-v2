from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from data.database import get_db
from data.hospital_model import Doctor
from schemas.hospital import DoctorCreate
from services.harsh import hash_password
from auth.dependencies import get_current_hospital

router = APIRouter(prefix="/doctor", tags=["Doctor"])

@router.post("/add")
def add_doctor(
    doctor_data: DoctorCreate,
    hospital_id: int = Depends(get_current_hospital),
    db: Session = Depends(get_db)
):
    existing_doctor = db.query(Doctor).filter(Doctor.email == doctor_data.email).first()
    if existing_doctor:
        raise HTTPException(status_code=400, detail="Doctor with this email already exists")
    hashed_password = hash_password(doctor_data.password)

    new_doctor = Doctor(
        first_name=doctor_data.first_name,
        last_name=doctor_data.last_name,
        gender=doctor_data.gender,
        department=doctor_data.department,
        phone_number=doctor_data.phone_number,
        email=doctor_data.email,
        password_hash=hashed_password,
        hospital_id=hospital_id
    )
    
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return{"message": "Doctor added successfully", "doctor_id": new_doctor.doctor_id}

