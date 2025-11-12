from .database import engine, Base
from .hospital_model import Hospital, Department, Doctor, Patient, MedicalRecord, LabTestResult, Prescription, LabTestFile

print("Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("All tables created successfully!")
