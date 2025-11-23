#!/usr/bin/env python3

import os
from dotenv import load_dotenv
from fastapi import HTTPException
from rapidfuzz import fuzz
from sqlalchemy import func
from data.database import SessionLocal
from data.hospital_model import Department as dept
from schemas.department import Department

load_dotenv()

class DepartmentService:
    """Service class for Department Operations"""

    def get_departments(self) -> list[dept]:
        """Get all departments"""
        with SessionLocal() as db:
            return db.query(dept).all()

    def get_department(self, department_name: str) -> list[dept]:
        """Search departments using partial matching with RapidFuzz."""
        threshold = int(os.getenv("threshold", 50))  # default 50 if not set

        with SessionLocal() as db:
            # Filter in SQL first
            candidates = db.query(dept).filter(
                func.trim(dept.department_name).ilike(f"%{department_name}%")
            ).all()

            # Apply RapidFuzz partial matching
            department_list = [
                d for d in candidates
                if fuzz.partial_ratio(department_name.lower(), (d.department_name or '').lower()) >= threshold
            ]

        if not department_list:
            raise HTTPException(status_code=404, detail="No matching departments found")

        return department_list

    def add_department(self, department_data: Department) -> dept:
        """Add a new department."""
        with SessionLocal() as db:
            # Check for duplicate
            existing = db.query(dept).filter(
                func.lower(dept.department_name) == department_data.department_name.lower()
            ).first()
            if existing:
                raise HTTPException(status_code=400, detail="Department already exists")

            new_department = dept(
                department_name=department_data.department_name,
                department_description=department_data.department_description,
                email=department_data.department_email,
                phone=department_data.phone,
                hospital_id=department_data.hospital_id,
                location=department_data.location,
                number_of_staff=department_data.number_of_staff,
                status=department_data.status
            )
            db.add(new_department)
            db.commit()
            db.refresh(new_department)

        return new_department

    def edit_department(self, department_data: Department, department_name: str) -> dept:
        """Edit an existing department."""
        with SessionLocal() as db:
            department = db.query(dept).filter(
                func.lower(dept.department_name) == department_name.lower()
            ).first()
            if not department:
                raise HTTPException(status_code=404, detail=f"Department '{department_name}' not found")

            # Update fields
            department.department_name = department_data.department_name
            department.department_description = department_data.department_description
            department.email = department_data.department_email
            department.phone = department_data.phone
            department.hospital_id = department_data.hospital_id
            department.location = department_data.location
            department.number_of_staff = department_data.number_of_staff
            department.status = department_data.status

            db.commit()
            db.refresh(department)

        return {"message": "New department created successfuly",
                "department": department
                }

    def delete_department(self, department_name: str) -> dict:
        """Deactivate a department."""
        with SessionLocal() as db:
            department = db.query(dept).filter(
                func.lower(dept.department_name) == department_name.lower()
            ).first()
            if not department:
                raise HTTPException(status_code=404, detail=f"Department '{department_name}' not found")

            # Soft delete
            department.status = False
            db.commit()
            db.refresh(department)

        return {"detail": f"Department '{department_name}' marked as inactive",
                "department": department
                }
