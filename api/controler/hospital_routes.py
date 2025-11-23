#!/usr/bin/env python3

from fastapi import APIRouter, HTTPException, Depends, Header
from sqlalchemy.orm import Session
from data.database import get_db
from data.hospital_model import Hospital
from schemas.hospital import HospitalLogin
from schemas.hospital import HospitalCreate
from services.harsh import hash_password, verify_password
from services.jwt import create_access_token
from services.token_blacklist import add_to_blacklist
from datetime import datetime

router = APIRouter()

@router.post("/signup")
def signup_hospital(hospital: HospitalCreate, db: Session = Depends(get_db)):
    existing_hospital = db.query(Hospital).filter(Hospital.hospital_email == hospital.hospital_email).first()

    if existing_hospital:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    hashed_password = hash_password(hospital.password)

    new_hospital = Hospital(
        hospital_name=hospital.hospital_name,
        hospital_email=hospital.hospital_email,
        hospital_country=hospital.hospital_country,
        hospital_city=hospital.hospital_city,
        hospital_license=hospital.hospital_license,
        password_hash=hashed_password,
        created_at=datetime.utcnow()
    )

    db.add(new_hospital)
    db.commit()
    db.refresh(new_hospital)

    return {
    "massage": "Hospital created successfuly",
    "hospital_id": new_hospital.hospital_id
    }

@router.post("/login")
def login_hospital(login_data: HospitalLogin, db: Session = Depends(get_db)):
    hospital = db.query(Hospital).filter(Hospital.hospital_email == login_data.hospital_email).first()

    if not hospital or not verify_password(login_data.password, hospital.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = create_access_token({"hospital_id": hospital.hospital_id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "hospital_id": hospital.hospital_id
    }
@router.post("/logout")
def logout(authorization : str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=400, detail="Invalid authorization header")

    
    token = authorization.split(" ")[1]
    add_to_blacklist(token)

    return {"message": "Logged out successfully"}
