#!/usr/bin/env python3

import requests

patient_id = 1

Endpoint = f"http://localhost:8080/doctor_portal/patients/new_consultation/{patient_id}"

consultation_data = {
    "hospital_id": 6,
    "patient_id": patient_id,
    "doctor_id": 22,
    "diagnosis": "Common Cold",
    "treatment": "Rest and hydration",
    "notes": "Patient should recover in a week.",
    "follow_up_date": "2025-11-18",
    "created_by": "Dr. Laura Kwizera"
}

token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N0b3JfaWQiOjIyLCJleHAiOjE3NjI4Nzg2MTl9.D_8WPFPGsL0udYod9z2ZTDjXBfFKhYq381wRQVCC8Lk"

headers = {
    "Authorization": f"Bearer {token}"
}

response = requests.post(Endpoint, json=consultation_data, headers=headers)

print("Status Code:", response.status_code)
print("Response Body:", response.json())
