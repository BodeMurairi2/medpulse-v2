from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from data.database import get_db
from services.patient_service import get_patient_records_by_id
from schemas.medical_record import PatientRecordsOut

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

