from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.web.hospital_routes import router as hospital_router
from api.web.doctor_routes import router as doctor_router
from api.web import patient_routes

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(hospital_router, prefix="/hospital")
app.include_router(doctor_router)
app.include_router(patient_routes.router, prefix="/patient", tags=["Patient"])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5500"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)