#!/usr/bin/env python3
import requests
from datetime import date

# ----------------- CONFIG -----------------
BASE_URL = "http://127.0.0.1:8080/doctor_portal"
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N0b3JfaWQiOjIyLCJleHAiOjE3NjI5NDQ4MTd9.BUrOlToE0wGCx2VkTNM8kWC4xuzz067UnjjNv0FXF-A"

HEADERS = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# ----------------- EXISTING IDS -----------------
record_id = 1          # Existing consultation record_id
prescription_id = 1    # Existing prescription_id
lab_test_id = 1        # Existing lab_test_id
lab_test_file_id = 1   # Existing lab_test_file_id

# ----------------- UPDATE DATA -----------------
updated_consultation = {
    "patient_id": 1,
    "doctor_id": 1,
    "diagnosis": "Updated diagnosis",
    "treatment": "Updated treatment",
    "notes": "Updated notes",
    "created_by": "Dr. John Doe",
    "follow_up_date": str(date.today()),
    "record_date": str(date.today())
}

updated_prescription = {
    "patient_id": 1,
    "doctor_id": 1,
    "record_id": record_id,
    "medicine_name": "Updated Medicine",
    "frequency": "2 times/day",
    "duration": "7 days",
    "dosage": "500mg",
    "notes": "Updated notes",
    "prescribed_by": "Dr. John Doe",
    "prescription_date": str(date.today()),
    "prescription_details": "Updated prescription details"
}

updated_lab_test = {
    "patient_id": 1,
    "doctor_id": 1,
    "record_id": record_id,
    "hospital_id": 1,
    "hospital_name": "Updated Hospital",
    "test_name": "Updated Blood Test",
    "result_value": "Updated Pending",
    "result_date": str(date.today()),
    "notes": "Updated lab test notes",
    "doctor_name": "Dr. John Doe"
}

lab_test_file_path = "/home/bode-murairi/Pictures/download.jpeg"  # Update to your file path

# ----------------- TEST UPDATE CONSULTATION -----------------
response_consultation = requests.put(
    f"{BASE_URL}/patients/update_consultation/{record_id}",
    headers=HEADERS,
    json=updated_consultation
)
print("Update Consultation:", response_consultation.status_code, response_consultation.text)

# ----------------- TEST UPDATE PRESCRIPTION -----------------
response_prescription = requests.put(
    f"{BASE_URL}/patients/update_prescription/{prescription_id}",
    headers=HEADERS,
    json=updated_prescription
)
print("Update Prescription:", response_prescription.status_code, response_prescription.text)

# ----------------- TEST UPDATE LAB TEST -----------------
response_lab_test = requests.put(
    f"{BASE_URL}/patients/update_lab_test/{lab_test_id}",
    headers=HEADERS,
    json=updated_lab_test
)
print("Update Lab Test:", response_lab_test.status_code, response_lab_test.text)

# ----------------- TEST UPDATE LAB TEST FILE -----------------
try:
    with open(lab_test_file_path, "rb") as file_data:
        files = {"new_file": file_data}  # Must match endpoint field name
        response_lab_test_file = requests.put(
            f"{BASE_URL}/patients/update_lab_test_file/{lab_test_file_id}",
            headers=HEADERS,
            files=files
        )
    print("Update Lab Test File:", response_lab_test_file.status_code, response_lab_test_file.text)
except FileNotFoundError:
    print(f"File not found: {lab_test_file_path}. Please provide a valid file path.")
