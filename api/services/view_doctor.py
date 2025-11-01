#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from fastapi import HTTPException
from sqlalchemy.orm import Session
from data.database import SessionLocal
from data.hospital_model import Doctor as doctor
from schemas.doctor import DoctorClass
from services.search_user import search_user
from services.doctor_stat import get_doctor_stats

load_dotenv()

class View_doctor:
    def get_doctors(self):
        """View all doctors per department"""
        with SessionLocal() as db:
            load_doctors = db.query(doctor).all()

        if not load_doctors:
            raise HTTPException(status_code=400, detail="No doctors in the platform")

        doctors_list = {}
        for doc in load_doctors:
            dept_key = doc.department
            if dept_key not in doctors_list:
                doctors_list[dept_key] = []

            doctors_list[dept_key].append({
                "first_name": doc.first_name,
                "last_name": doc.last_name,
                "gender": doc.gender,
                "phone_number": doc.phone_number,
                "email": doc.email
            })
        return doctors_list

    def get_doctor(self, doctor_name:str) -> DoctorClass:
        """This will be implemented later using first_name and last_name"""
        with SessionLocal() as db:
            doctor_data = search_user(user_name=doctor_name,
                        database=doctor,
                        session = db
                        )
        
        if not doctor_data:
            return HTTPException(status_code=400, detail="Doctor not found")

        return doctor_data

    def get_doctor_statistics(self, doctor_name:str)-> dict:
        """This functions returns doctor statistics"""
        with SessionLocal() as db:
            doctor_data = search_user(user_name=doctor_name,
                                      database=doctor,
                                      session= db)
        
        if not doctor_data:
            return HTTPException(status_code=400, detail="Doctor not found")

        with SessionLocal() as db:
            return get_doctor_stats(db_session=db, doctor_id=doctor_data.doctor_id)
