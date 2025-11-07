from api.data.database import Base, engine
from api.data.hospital_model import Hospital, Department, Doctor, Patient, MedicalRecord, LabTestResult, Prescription


Base.metadata.create_all(bind=engine)

print("Tables creates successfuly!")