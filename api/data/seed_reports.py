#!/usr/bin/env python3

from data.database import SessionLocal
from data.hospital_model import (
    Hospital,
    Department,
    Doctor,
    Patient,
    MedicalRecord,
    LabTestResult,
    Prescription,
)
from datetime import datetime, date, timedelta
import random


def seed_reports_data():
    db = SessionLocal()

    try:
        print("🌱 Seeding database with test data...")

        # ---------------- Hospitals ----------------
        if db.query(Hospital).count() == 0:
            hospitals = [
                Hospital(
                    hospital_name="MedPulse General Hospital",
                    hospital_email="info@medpulse.com",
                    hospital_country="Rwanda",
                    hospital_city="Kigali",
                    hospital_license="MPG12345",
                    password_hash="hashed_password"
                ),
                Hospital(
                    hospital_name="EastCare Clinic",
                    hospital_email="contact@eastcare.com",
                    hospital_country="Rwanda",
                    hospital_city="Huye",
                    hospital_license="ECC67890",
                    password_hash="hashed_password"
                ),
            ]
            db.add_all(hospitals)
            db.commit()
            print(f"Created {len(hospitals)} hospitals")
        else:
            print("Hospitals already exist, skipping...")

        # ---------------- Departments ----------------
        if db.query(Department).count() == 0:
            departments = [
                Department(
                    department_name="Cardiology",
                    department_description="Heart and cardiovascular care"
                ),
                Department(
                    department_name="Pediatrics",
                    department_description="Children's health"
                ),
                Department(
                    department_name="General Medicine",
                    department_description="General medical care"
                ),
            ]
            db.add_all(departments)
            db.commit()
            print(f"Created {len(departments)} departments")
        else:
            print("Departments already exist, skipping...")

        # ---------------- Doctors ----------------
        if db.query(Doctor).count() == 0:
            doctors = [
                Doctor(
                    first_name="Sarah",
                    last_name="Johnson",
                    gender="Female",
                    hospital_id=1,
                    department="Cardiology",
                    email="sarah.johnson@medpulse.com",
                    phone_number="+250788111111",
                    password_hash="hashed_password"
                ),
                Doctor(
                    first_name="Michael",
                    last_name="Chen",
                    gender="Male",
                    hospital_id=1,
                    department="Pediatrics",
                    email="michael.chen@medpulse.com",
                    phone_number="+250788222222",
                    password_hash="hashed_password"
                ),
                Doctor(
                    first_name="Amina",
                    last_name="Mugisha",
                    gender="Female",
                    hospital_id=1,
                    department="General Medicine",
                    email="amina.mugisha@medpulse.com",
                    phone_number="+250788333333",
                    password_hash="hashed_password"
                ),
            ]
            db.add_all(doctors)
            db.commit()
            print(f"Created {len(doctors)} doctors")
        else:
            print("Doctors already exist, skipping...")

        # ---------------- Patients ----------------
        if db.query(Patient).count() == 0:
            first_names = [
                "Alice", "Bob", "Charlie", "Diana", "Emmanuel", "Faith",
                "Grace", "Henry", "Innocent", "Jane", "Kevin", "Lydia",
                "Moses", "Nancy", "Oliver", "Peace", "Queen", "Robert",
                "Sarah", "Thomas", "Uwase", "Victor", "Wendy", "Xavier",
                "Yves", "Zara"
            ]
            second_names = [
                "Uwase", "Mugisha", "Kayitesi", "Niyonzima", "Habimana",
                "Mukamana", "Nsanzimana", "Iradukunda", "Bizimana", "Mutoni",
                "Shema", "Kalisa", "Uwera", "Manzi"
            ]
            patients = []

            for i in range(40):
                first = random.choice(first_names)
                second = random.choice(second_names)
                patients.append(Patient(
                    first_name=first,
                    second_name=second,
                    date_of_birth=date(
                        random.randint(1950, 2018),
                        random.randint(1, 12),
                        random.randint(1, 28)
                    ),
                    gender=random.choice(["Male", "Female"]),
                    phone_number=f"+2507{random.randint(80000000, 89999999)}",
                    email=f"{first.lower()}.{second.lower()}{i}@example.com",
                    password_hash="hashed_password"
                ))
            db.add_all(patients)
            db.commit()
            print(f"Created {len(patients)} patients")
        else:
            print("Patients already exist, skipping...")

        # ---------------- Medical Records ----------------
        if db.query(MedicalRecord).count() == 0:
            patients_list = db.query(Patient).all()
            doctors_list = db.query(Doctor).all()
            records = []

            for patient in patients_list:
                for _ in range(random.randint(1, 3)):
                    records.append(MedicalRecord(
                        patient_id=patient.patient_id,
                        doctor_id=random.choice(doctors_list).doctor_id,
                        hospital_name=random.choice(hospitals).hospital_name,
                        diagnosis=random.choice([
                            "Hypertension", "Flu", "Diabetes", "Asthma", "Infection", "Checkup"
                        ]),
                        treatment=random.choice([
                            "Medication prescribed", "Rest and hydration", "Follow-up in 2 weeks"
                        ]),
                        record_date=datetime(2024, 10, random.randint(1, 30)),
                    ))
            db.add_all(records)
            db.commit()
            print(f"Created {len(records)} medical records")
        else:
            print("Medical records already exist, skipping...")

        # ---------------- Lab Test Results ----------------
        if db.query(LabTestResult).count() == 0:
            patients_list = db.query(Patient).all()
            lab_tests = []
            test_names = ["Blood test", "X-ray", "Urine test", "MRI", "CT scan"]

            for patient in patients_list:
                for _ in range(random.randint(1, 2)):
                    lab_tests.append(LabTestResult(
                        patient_id=patient.patient_id,
                        test_name=random.choice(test_names),
                        result_value=random.choice(["Normal", "Abnormal"]),
                        result_date=datetime(2024, 10, random.randint(1, 30))
                    ))
            db.add_all(lab_tests)
            db.commit()
            print(f"Created {len(lab_tests)} lab test results")
        else:
            print("Lab tests already exist, skipping...")

        # ---------------- Prescriptions ----------------
        if db.query(Prescription).count() == 0:
            patients_list = db.query(Patient).all()
            doctors_list = db.query(Doctor).all()
            prescriptions = []
            meds = ["Amoxicillin", "Ibuprofen", "Metformin", "Paracetamol", "Atorvastatin"]

            for patient in patients_list:
                for _ in range(random.randint(1, 2)):
                    prescriptions.append(Prescription(
                        patient_id=patient.patient_id,
                        doctor_id=random.choice(doctors_list).doctor_id,
                        medicine_name=random.choice(meds),
                        dosage="500mg",
                        duration=f"{random.randint(3, 10)} days",
                        prescription_date=datetime(2024, 10, random.randint(1, 30)),
                        notes=random.choice(["Take after meals", "Take before meals", None]),
                    ))
            db.add_all(prescriptions)
            db.commit()
            print(f"Created {len(prescriptions)} prescriptions")
        else:
            print("Prescriptions already exist, skipping...")

        print("\nDatabase seeding completed successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_reports_data()
