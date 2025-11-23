#!/usr/bin/env python3

import requests
from datetime import datetime

# Backend URL
BASE_URL = "http://127.0.0.1:8080/doctor_portal"

# JWT token of the logged-in doctor
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N0b3JfaWQiOjIyLCJleHAiOjE3NjI5NDI1MzF9.Q780cWXKyI66ZlX-TWunc_1yLV1kgJqXGT_t8XPi4iM"

# Headers
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# Patient and doctor info
patient_id = 1
doctor_id = 22
doctor_name = "Dr. John Doe"

# Data for creating the lab test
lab_test_data = {
    "patient_id": patient_id,
    "doctor_id": doctor_id,
    "doctor_name": doctor_name,
    "test_name": "Blood Test",
    "result_value": "Pending",
    "result_date": datetime.utcnow().date().isoformat(),
    "notes": "Routine check"
}

# File to upload
file_path = "/home/bode-murairi/Pictures/download.jpeg"  # adjust path
files = {"file": open(file_path, "rb")}

# ----------------------------
# Step 1: Create new lab test
# ----------------------------
response_lab_test = requests.post(
    f"{BASE_URL}/patients/new_lab_test/{patient_id}",
    headers=headers,
    json=lab_test_data
)

if response_lab_test.status_code == 200:
    lab_test = response_lab_test.json()
    lab_test_id = lab_test.get("test_id")  # make sure endpoint returns test_id

    if lab_test_id is None:
        print("Error: lab_test_id not returned from API")
        exit(1)

    # ----------------------------
    # Step 2: Upload file
    # ----------------------------
    response_file = requests.post(
        f"{BASE_URL}/patients/lab_test/{lab_test_id}/upload_file",
        headers=headers,
        files=files
    )

    if response_file.status_code == 200:
        public_url = response_file.text  # endpoint returns only the URL
        print("File uploaded successfully:", public_url)
    else:
        print("Failed to upload file:", response_file.status_code, response_file.text)

else:
    print("Failed to create lab test:", response_lab_test.status_code, response_lab_test.text)
