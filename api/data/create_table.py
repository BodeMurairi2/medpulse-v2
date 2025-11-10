#!/usr/bin/env python3
from .database import Base, engine
from .hospital_model import Hospital, Department, Doctor, Patient, MedicalRecord, LabTestResult, Prescription

# Create all tables
Base.metadata.create_all(bind=engine)

print("All tables created successfully!")
