#!/usr/bin/env python3
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from web.hospital_routes import router as hospital_router
from web.doctor_routes import router as doctor_router
from web import patient_routes
from controler.department import department_router
from controler.view_doctor import router as doctor_view_router
from controler.reports import router as reports_router
from controler.hospital_routes import router as hospital_router
from controler.doctor_portal import doctor_portal_router as doctor_portal_router
from controler.doctor_routes import router as doctor_router
from controler.patient_controller import router as patient_router
from dotenv import load_dotenv

load_dotenv()
print("Loading Environment Variables...")

print("Environment Variables Loaded:")
print("DATABASE_URL:", os.getenv("DATABASE_URL"))

app = FastAPI(title="MedPulse API",
              description="Hospital Database Management system",
              version="1.0.0"
              )

app = FastAPI()

origins = [
    "http://localhost:5500",
    "http://localhost:8000",
    "http://localhost:3000",
    "http://127.0.0.1:5500",
    "http://127.0.0.1:8000",
    "http://127.0.0.1:3000"
    ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(department_router)
app.include_router(doctor_view_router)
app.include_router(reports_router)
app.include_router(hospital_router)
app.include_router(doctor_portal_router)
app.include_router(doctor_router)
app.include_router(hospital_router, prefix="/hospital")
app.include_router(doctor_router)
app.include_router(patient_router)

@app.get("/")
async def root():
    return {"message": "Welcome to MedPulse API"}

if __name__ == "__main__":
    uvicorn.run("web.web:app",
                port=8080,
                reload=True
                )
