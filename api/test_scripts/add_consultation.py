#!/usr/bin/env python3

import requests

patient_id = 1
doctor_id = 22

Endpoint = f"http://localhost:8080/doctor_portal/patients/new_prescription/{patient_id}"

consultation_data = {
    "patient_id": patient_id,
    "doctor_id": doctor_id,
    "medicine_name": "Restamox",
    "frequency": "Twice a day",
    "duration": "7 days",
    "dosage": "500mg",
    "notes": "Patient should recover in a week.",
    "prescribed_by": "Dr. Laura Kwizera",
    "prescription_date": "2025-11-18",           # optional
    "prescription_details": "Take after meals"  # optional
}

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N0b3JfaWQiOjIyLCJleHAiOjE3NjI5MjIyNjF9.HhY5PVshztg6rqovJfUacynwlT57TR5T3XXbsXifwwc"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.post(Endpoint, json=consultation_data, headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.json())
