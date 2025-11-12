#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import boto3
from botocore.client import Config
from urllib.parse import quote

load_dotenv()

R2_ACCESS_KEY_ID = os.getenv("CLOUDFLARE_ACCESS_KEYID")
R2_SECRET_ACCESS_KEY = os.getenv("SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME")
R2_ENDPOINT_URL = os.getenv("R2_ENDPOINT")
R2_PUBLIC_URL_BASE = os.getenv("R2_PUBLIC_URL_BASE").rstrip("/")

s3 = boto3.client(
    's3',
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    endpoint_url=R2_ENDPOINT_URL,
    config=Config(signature_version='s3v4')
)


def sanitize_for_url(text: str) -> str:
    """Replace spaces with dashes and URL-encode special characters."""
    return quote(text.replace(" ", "-"))


def upload_user_document(file, file_name, file_extension, patient_name, report_type):
    allowed_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".tif", ".webp",
                          ".heic", ".heif", ".dcm", ".pdf", ".doc", ".docx", ".rtf", ".odt",
                          ".txt", ".md", ".xls", ".xlsx", ".csv", ".xml", ".json", ".hl7"]

    if not file_extension.startswith('.'):
        file_extension = '.' + file_extension

    if file_extension.lower() not in [ext.lower() for ext in allowed_extensions]:
        return f"Document {file_name} with extension {file_extension} not supported."

    safe_patient_name = quote(patient_name.replace(" ", "-"))
    safe_report_type = quote(report_type.replace(" ", "-"))
    safe_file_name = quote(file_name.replace(" ", "-"))

    path_to_upload = f"patients/{safe_patient_name}/report/{safe_report_type}/{safe_file_name}"

    # Upload file with public-read
    s3.put_object(
        Bucket=R2_BUCKET_NAME,
        Key=path_to_upload,
        Body=file.stream,
        ACL='public-read'
    )

    # Include bucket name in public URL
    public_url = f"{os.getenv('R2_PUBLIC_URL_BASE').rstrip('/')}/{R2_BUCKET_NAME}/{path_to_upload}"
    return public_url

# Example usage
if __name__ == "__main__":
    # file = <Flask FileStorage object>
    # file_name = file.filename
    # file_extension = os.path.splitext(file.filename)[1]
    # patient_name = "John Doe"
    # report_type = "Lab Result"
    # print(upload_user_document(file, file_name, file_extension, patient_name, report_type))
    pass
