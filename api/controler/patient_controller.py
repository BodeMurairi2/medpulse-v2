from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.database import get_db
from services.patient_service import get_patient_records_by_email
from schemas.patient_records import PatientRecordsOut

router = APIRouter()

@router.get("/patients/{email}/records", response_model=PatientRecordsOut)
def get_patient_records(email: str, db: Session = Depends(get_db)):
    try:
        patient = get_patient_records_by_email(db, email)
        if not patient:
            raise HTTPException(status_code=404, detail="Patient not found")
        return patient
    except Exception as e:
        print("❌ ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
