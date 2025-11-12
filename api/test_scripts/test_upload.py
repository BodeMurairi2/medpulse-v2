#!/usr/bin/env python3

from fastapi import UploadFile
from services.upload import upload_user_document

# Open a file from your computer
file_path = "/home/bode-murairi/Pictures/download.jpeg"
hospital_name = "Test Hospital"
patient_name = "John Doe"
report_type = "LabReport"

# FastAPI UploadFile simulation
class FakeUploadFile:
    def __init__(self, file_path):
        self.filename = file_path.split("/")[-1]
        self.file = open(file_path, "rb")

# Create a fake UploadFile
fake_file = FakeUploadFile(file_path)

# Upload to Cloudflare R2
try:
    public_url = upload_user_document(fake_file, hospital_name, patient_name, report_type)
    print("File uploaded successfully!")
    print("Public URL:", public_url)
finally:
    fake_file.file.close()
