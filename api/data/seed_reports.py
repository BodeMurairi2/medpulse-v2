#!/usr/bin/env python3

from api.data.database import SessionLocal
from api.data.models import Department, Staff, Patient, Appointment, Consultation, Prescription, LabTest
from datetime import datetime, date, timedelta
import random

def seed_reports_data():
    db = SessionLocal()

    try:
        print("Seeding database with test data...")


        if db.query(Department).count() == 0:
            departments = [
                Department(name="Cardiology", description="Heart and cardiovascular care"),
                Department(name="Pediatrics", description="Children's health"),
                Department(name="General Medicine", description="General medical care"),
            ]
            db.add_all(departments)
            db.commit()
            print(f"Created {len(departments)} departments")
        else:
            print("Departments already exist, skipping...")


        if db.query(Staff).count() == 0:
            doctors = [
                Staff(
                    full_name="Dr. Sarah Johnson",
                    role="Doctor",
                    specialization="Cardiology",
                    email="sarah.johnson@medpulse.com",
                    phone="+250788111111",
                    department_id=1
                ),
                Staff(
                    full_name="Dr. Michael Chen",
                    role="Doctor",
                    specialization="Pediatrics",
                    email="michael.chen@medpulse.com",
                    phone="+250788222222",
                    department_id=2
                ),
                Staff(
                    full_name="Dr. Amina Mugisha",
                    role="Doctor",
                    specialization="General Medicine",
                    email="amina.mugisha@medpulse.com",
                    phone="+250788333333",
                    department_id=3
                ),
            ]
            db.add_all(doctors)
            db.commit()
            print(f"Created {len(doctors)} doctors")
        else:
            print("Doctors already exist, skipping...")


        if db.query(Patient).count() == 0:
            patients = []
            first_names = ["Alice", "Bob", "Charlie", "Diana", "Emmanuel", "Faith",
                        "Grace", "Henry", "Innocent", "Jane", "Kevin", "Lydia",
                        "Moses", "Nancy", "Oliver", "Peace", "Queen", "Robert",
                        "Sarah", "Thomas", "Uwase", "Victor", "Wendy", "Xavier",
                        "Yves", "Zara"]
            last_names = ["Uwase", "Mugisha", "Kayitesi", "Niyonzima", "Habimana",
                        "Mukamana", "Nsanzimana", "Iradukunda", "Bizimana", "Mutoni",
                        "Shema", "Kalisa", "Uwera", "Manzi"]

            for i in range(40):
                first_name = random.choice(first_names)
                last_name = random.choice(last_names)
                patients.append(Patient(
                    full_name=f"{first_name} {last_name}",
                    date_of_birth=date(
                        random.randint(1950, 2018),
                        random.randint(1, 12),
                        random.randint(1, 28)
                    ),
                    gender=random.choice(["Male", "Female"]),
                    contact=f"+2507{random.randint(80000000, 89999999)}",
                    email=f"{first_name.lower()}.{last_name.lower()}{i}@example.com",
                    created_at=datetime(2024, random.randint(8, 10), random.randint(1, 28))
                ))

            db.add_all(patients)
            db.commit()
            print(f"Created {len(patients)} patients")
        else:
            print("Patients already exist, skipping...")


        if db.query(Appointment).count() == 0:
            statuses = ["completed", "completed", "completed", "completed", "cancelled", "no-show", "scheduled"]
            appointments = []
            start_date = datetime(2024, 10, 1, 8, 0)
            doctors_list = db.query(Staff).filter(Staff.role == "Doctor").all()
            patient_count = db.query(Patient).count()

            for day in range(30):
                current_date = start_date + timedelta(days=day)
                for doctor in doctors_list:
                    num_appointments = random.randint(10, 15)
                    for appt_num in range(num_appointments):
                        hour = 8 + (appt_num // 2)
                        minute = 0 if appt_num % 2 == 0 else 30
                        if hour >= 17:
                            break
                        appointment_time = current_date.replace(hour=hour, minute=minute)
                        appointments.append(Appointment(
                            patient_id=random.randint(1, patient_count),
                            doctor_id=doctor.id,
                            department_id=doctor.department_id,
                            appointment_date=appointment_time,
                            status=random.choice(statuses),
                            notes=random.choice([
                                "Regular checkup",
                                "Follow-up consultation",
                                "Post-surgery follow-up",
                                "Urgent care visit",
                                "Routine examination",
                                "Annual physical examination",
                                None
                            ]),
                            created_at=appointment_time - timedelta(days=random.randint(1, 14))
                        ))

            db.add_all(appointments)
            db.commit()
            print(f"Created {len(appointments)} appointments")
        else:
            print("Appointments already exist, skipping...")


        if db.query(Consultation).count() == 0:
            consultations = []
            start_date = datetime(2024, 10, 1)
            doctors_list = db.query(Staff).filter(Staff.role == "Doctor").all()
            patients_list = db.query(Patient).all()

            for patient in patients_list:
                for _ in range(random.randint(1, 3)):
                    consultations.append(Consultation(
                        patient_id=patient.id,
                        doctor_id=random.choice(doctors_list).id,
                        date=start_date + timedelta(days=random.randint(0, 29)),
                        notes=random.choice(["Follow-up", "Routine check", "Urgent visit"])
                    ))
            db.add_all(consultations)
            db.commit()
            print(f"Created {len(consultations)} consultations")
        else:
            print("Consultations already exist, skipping...")


        if db.query(Prescription).count() == 0:
            prescriptions = []
            meds = ["Amoxicillin", "Ibuprofen", "Metformin", "Paracetamol", "Atorvastatin"]
            patients_list = db.query(Patient).all()
            doctors_list = db.query(Staff).filter(Staff.role == "Doctor").all()

            for patient in patients_list:
                for _ in range(random.randint(1, 2)):
                    prescriptions.append(Prescription(
                        patient_id=patient.id,
                        doctor_id=random.choice(doctors_list).id,
                        medication=random.choice(meds),
                        dosage="500mg",
                        duration=f"{random.randint(3, 10)} days",
                        date_issued=datetime(2024, 10, random.randint(1, 30))
                    ))
            db.add_all(prescriptions)
            db.commit()
            print(f"Created {len(prescriptions)} prescriptions")
        else:
            print("Prescriptions already exist, skipping...")

        if db.query(LabTest).count() == 0:
            lab_tests = []
            tests = ["Blood test", "X-ray", "Urine test", "MRI", "CT scan"]
            patients_list = db.query(Patient).all()

            for patient in patients_list:
                for _ in range(random.randint(1, 2)):
                    lab_tests.append(LabTest(
                        patient_id=patient.id,
                        test_name=random.choice(tests),
                        result=random.choice(["Normal", "Abnormal"]),
                        reference_range="N/A",
                        date_conducted=datetime(2024, 10, random.randint(1, 30))
                    ))
            db.add_all(lab_tests)
            db.commit()
            print(f"Created {len(lab_tests)} lab tests")
        else:
            print("Lab tests already exist, skipping...")

        print("\nDatabase seeding completed successfully!")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_reports_data()
