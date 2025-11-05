from data.database import SessionLocal
from data.models import Department, Staff, Patient, Appointment
from datetime import datetime, date, timedelta
import random

def seed_reports_data():
    db = SessionLocal()

    try:
        print("Seeding database with test data...")

        departments = [
            Department(name="Cardiology", description="Heart and cardiovascular care"),
            Department(name="Pediatrics", description="Children's health"),
            Department(name="General Medicine", description="General medical care"),
        ]
        db.add_all(departments)
        db.commit()
        print(f"Created {len(departments)} departments")

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

        patients = [
            Patient(
                full_name="Jane Smith",
                date_of_birth=date(2004, 5, 15),
                gender="Female",
                contact="+250788123456",
                email="jane.smith@example.com",
                created_at=datetime(2024, 9, 1)
            ),
            Patient(
                full_name="John Doe",
                date_of_birth=date(1999, 8, 20),
                gender="Male",
                contact="+250788654321",
                email="john.doe@example.com",
                created_at=datetime(2024, 9, 15)
            ),
            Patient(
                full_name="Alice Uwase",
                date_of_birth=date(2002, 3, 10),
                gender="Female",
                contact="+250788987654",
                email="alice.uwase@example.com",
                created_at=datetime(2024, 10, 1)
            ),
            Patient(
                full_name="Bob Shema",
                date_of_birth=date(1997, 12, 5),
                gender="Male",
                contact="+250788555555",
                email="bob.shema@example.com",
                created_at=datetime(2024, 10, 10)
            ),
        ]
        db.add_all(patients)
        db.commit()
        print(f"Created {len(patients)} patients")

        statuses = ["completed", "completed", "completed", "cancelled", "no-show", "scheduled"]
        appointments = []
        start_date = datetime(2024, 10, 1, 9, 0)

        doctors_list = db.query(Staff).filter(Staff.role == "Doctor").all()

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
                    patient_id=random.randint(len(patients)),
                    doctor_id=doctor.id,
                    department_id=doctor.department_id,
                    appointment_date=appointment_time,
                    status=random.choice(statuses),
                    notes=random.choice([
                        "Regular checkup",
                        "Follow-up consultation",
                        "Post-surgery follow-up",
                        "Urgent care visit",
                        None
                    ]),
                    created_at=appointment_time - timedelta(days=random.randint(1, 14))
                ))

        db.add_all(appointments)
        db.commit()
        print(f"Created {len(appointments)} appointments")

        print("\n Database seeded successfully!")
        print(f"Departments: {len(departments)}")
        print(f"Doctors: {len(doctors)}")
        print(f"Patients: {len(patients)}")
        print(f"Appointments: {len(appointments)}")
        print(f"Appointments per doctor per day: ~{len(appointments) // (len(doctors_list) * 30)}")

    except Exception as e:
        print(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_reports_data()
