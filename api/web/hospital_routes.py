from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api.data.database import get_db
from api.data.hospital_model import Hospital
from api.schemas.hospital import HospitalCreate
from api.services.harsh import hash_password
from datetime import datetime

router = APIRouter()

@router.post("/signup")
def signup_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    existing_hospital = db.query(Hospital).filter(Hospital.hospital_email == hospital.hospital_email).first()

    if existing_hospital:
        raise HTTPException(status_code=404, detail="Email already exists")
    
    harshed_password = hash_password(hospital.password)

    new_hopital = Hospital(
        hospital_name=Hospital.hospital_name,
        hospital_email=Hospital.hospital_email,
        hospital_country=Hospital.hospital_country,
        hospital_city=Hospital.hospital_city,
        hospital_licence=Hospital.hospital_license,
        password_harsh=Hospital.password_hash,
        created_at=datetime.utcnow
    )

    db.add(new_hopital)
    db.commit()
    db.refresh()

    return {
    "massage": "Hospital created successfuly",
    "hospital_id": new_hopital.hospital_id
    }

