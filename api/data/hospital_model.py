#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date, Text, func
from sqlalchemy.orm import relationship
from .database import Base

# Hospitals
class Hospital(Base):
    __tablename__ = "hospitals"
    hospital_id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_name = Column(String, nullable=False)
    hospital_email = Column(String, nullable=False)
    hospital_country = Column(String)
    hospital_city = Column(String)
    hospital_license = Column(String)
    password_hash = Column(String)
    completed_at = Column(DateTime)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    doctors = relationship("Doctor", back_populates="hospital")
    departments = relationship("Department", back_populates="hospital")
    medical_records = relationship("MedicalRecord", back_populates="hospital")
    lab_tests = relationship("LabTestResult", back_populates="hospital")
    prescriptions = relationship("Prescription", back_populates="hospital")

    def __repr__(self):
        return f"<Hospital(id={self.hospital_id}, name={self.hospital_name})>"

# Departments
class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String, nullable=False)
    department_description = Column(Text)
    hospital_id = Column(Integer, ForeignKey("hospitals.hospital_id"))
    email = Column(String)
    phone = Column(String)
    location = Column(String)
    status = Column(Boolean, default=True)
    number_of_staff = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    hospital = relationship("Hospital", back_populates="departments")
    def __repr__(self):
        return f"<Department(id={self.department_id}, name={self.department_name})>"

# Doctors
class Doctor(Base):
    __tablename__ = "doctors"
    doctor_id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    gender = Column(String)
    hospital_id = Column(Integer, ForeignKey("hospitals.hospital_id"))
    department = Column(String)
    phone_number = Column(String)
    password_hash = Column(String)
    email = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    hospital = relationship("Hospital", back_populates="doctors")
    medical_records = relationship("MedicalRecord", back_populates="doctor")
    prescriptions = relationship("Prescription", back_populates="doctor")
    lab_tests = relationship("LabTestResult", back_populates="doctor")

    def __repr__(self):
        return f"<Doctor(id={self.doctor_id}, name={self.first_name} {self.last_name})>"

# Patients
class Patient(Base):
    __tablename__ = "patients"
    patient_id = Column(Integer, primary_key=True, autoincrement=True)
    id_type = Column(String)
    first_name = Column(String, nullable=False)
    middle_name = Column(String)
    second_name = Column(String)
    gender = Column(String)
    date_of_birth = Column(Date)
    home_address = Column(String)
    email = Column(String)
    password_hash = Column(String)
    phone_number = Column(String)
    emergency_contact_name = Column(String)
    emergency_contact_phone = Column(String)
    profile_picture = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    medical_records = relationship("MedicalRecord", back_populates="patient")
    prescriptions = relationship("Prescription", back_populates="patient")
    lab_tests = relationship("LabTestResult", back_populates="patient")

    def __repr__(self):
        return f"<Patient(id={self.patient_id}, name={self.first_name} {self.second_name})>"

# Medical Records 
class MedicalRecord(Base):
    __tablename__ = "medical_records"
    record_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.hospital_id"))
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))
    hospital_name = Column(String)
    diagnosis = Column(String)
    treatment = Column(String)
    notes = Column(Text)
    follow_up_date = Column(Date)
    created_by = Column(String)
    record_date = Column(Date)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    patient = relationship("Patient", back_populates="medical_records")
    hospital = relationship("Hospital", back_populates="medical_records")
    doctor = relationship("Doctor", back_populates="medical_records")
    prescriptions = relationship("Prescription", back_populates="medical_record")
    lab_tests = relationship("LabTestResult", back_populates="medical_record")

    def __repr__(self):
        return f"<MedicalRecord(id={self.record_id}, patient_id={self.patient_id}, doctor_id={self.doctor_id})>"

# Lab Test Results
class LabTestResult(Base):
    __tablename__ = "lab_test_results"
    test_id = Column(Integer, primary_key=True, autoincrement=True)
    record_id = Column(Integer, ForeignKey("medical_records.record_id"))
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.hospital_id"))
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))
    hospital_name = Column(String)
    test_name = Column(String)
    result_value = Column(String)
    result_date = Column(Date)
    notes = Column(Text)
    doctor_name = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    patient = relationship("Patient", back_populates="lab_tests")
    hospital = relationship("Hospital", back_populates="lab_tests")
    doctor = relationship("Doctor", back_populates="lab_tests")
    medical_record = relationship("MedicalRecord", back_populates="lab_tests")
    files = relationship("LabTestFile", back_populates="lab_test", cascade="all, delete-orphan")  # NEW

    def __repr__(self):
        return f"<LabTestResult(id={self.test_id}, test_name={self.test_name})>"

# NEW TABLE: Lab Test Files
class LabTestFile(Base):
    __tablename__ = "lab_test_files"
    file_id = Column(Integer, primary_key=True, autoincrement=True)
    lab_test_id = Column(Integer, ForeignKey("lab_test_results.test_id", ondelete="CASCADE"))
    file_url = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    lab_test = relationship("LabTestResult", back_populates="files")

    def __repr__(self):
        return f"<LabTestFile(id={self.file_id}, lab_test_id={self.lab_test_id}, url={self.file_url})>"

# Prescriptions
class Prescription(Base):
    __tablename__ = "prescriptions"
    prescription_id = Column(Integer, primary_key=True, autoincrement=True)
    patient_id = Column(Integer, ForeignKey("patients.patient_id"))
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"))
    hospital_id = Column(Integer, ForeignKey("hospitals.hospital_id"))
    record_id = Column(Integer, ForeignKey("medical_records.record_id"))
    hospital_name = Column(String)
    medicine_name = Column(String)
    frequency = Column(String)
    duration = Column(String)
    notes = Column(Text)
    dosage = Column(String)
    prescription_date = Column(Date)
    prescription_details = Column(Text)
    prescribed_by = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    patient = relationship("Patient", back_populates="prescriptions")
    hospital = relationship("Hospital", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")
    medical_record = relationship("MedicalRecord", back_populates="prescriptions")

    def __repr__(self):
        return f"<Prescription(id={self.prescription_id}, medicine={self.medicine_name})>"
