from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from data.database import get_db
from services.patient_service import get_patient_records_by_id
from schemas.medical_record import PatientRecordsOut
import qrcode
import uuid
import os

router = APIRouter()

@router.get("/patients/{patient_id}/records", response_model=PatientRecordsOut)
def get_patient_records(patient_id: int, db: Session = Depends(get_db)):
    """
    Fetch patient records by patient_id
    """
    try:
        patient = get_patient_records_by_id(db, patient_id)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{patient_id}/generate-qr")
def generate_qr(patient_id: int):
    """
    Generate a QR code that links to this patient's medical records (for testing).
    """
    token = str(uuid.uuid4())

    share_url = f"http://localhost:8000/patients/{patient_id}/records?token={token}"

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(share_url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    os.makedirs("qrcodes", exist_ok=True)
    qr_path = f"qrcodes/patient_{patient_id}_qr.png"
    img.save(qr_path)

    return FileResponse(qr_path, media_type="image/png", filename=f"patient_{patient_id}_qr.png")