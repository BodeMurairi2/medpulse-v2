#!/usr/bin/env python3
import os
from urllib.parse import quote
from fastapi import UploadFile, HTTPException
import boto3
from botocore.client import Config
from dotenv import load_dotenv

load_dotenv()

# Cloudflare R2 credentials
R2_ACCESS_KEY_ID = os.getenv("CLOUDFLARE_ACCESS_KEYID")
R2_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT")
R2_PUBLIC_URL_BASE = os.getenv("R2_PUBLIC_URL_BASE").rstrip("/")

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    endpoint_url=R2_ENDPOINT_URL,
    config=Config(signature_version="s3v4")
)

# Allowed file extensions
ALLOWED_EXTENSIONS = [
    ".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp",
    ".heic", ".heif", ".dcm", ".pdf", ".doc", ".docx", ".rtf", ".odt",
    ".txt", ".md", ".xls", ".xlsx", ".csv", ".xml", ".json", ".hl7"
]

def sanitize_for_url(text: str) -> str:
    """Replace spaces with dashes and URL-encode special characters."""
    return quote(text.replace(" ", "-"))

def upload_user_document(file: UploadFile, hospital_name: str, patient_name: str, report_type: str) -> str:
    """
    Upload a file to Cloudflare R2 with folder structure:
    hospitals/<hospital_name>/patients/<patient_name>/report/<report_type>/<file_name>
    
    Returns the public URL of the uploaded file.
    """
    # Extract file name and extension
    file_name = file.filename
    _, file_extension = os.path.splitext(file_name)

    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    # Validate file extension
    if file_extension.lower() not in [ext.lower() for ext in ALLOWED_EXTENSIONS]:
        raise HTTPException(status_code=400, detail=f"File type {file_extension} not supported.")

    # Sanitize folder/file names
    safe_hospital_name = sanitize_for_url(hospital_name)
    safe_patient_name = sanitize_for_url(patient_name)
    safe_report_type = sanitize_for_url(report_type)
    safe_file_name = sanitize_for_url(file_name)

    # Construct the full path
    path_to_upload = f"hospitals/{safe_hospital_name}/patients/{safe_patient_name}/report/{safe_report_type}/{safe_file_name}"

    try:
        s3.put_object(
            Bucket=R2_BUCKET_NAME,
            Key=path_to_upload,
            Body=file.file,
            ACL="public-read"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

    # Build public URL
    public_url = f"{R2_PUBLIC_URL_BASE}/{R2_BUCKET_NAME}/{path_to_upload}"
    return public_url
