#!/usr/bin/env python3

from data.database import SessionLocal
from data.hospital_model import Department

db = SessionLocal()

load_department = db.query(Department).all()

def load_department_data():
    """Load all department"""
    return load_department

