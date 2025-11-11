#!/usr/bin/env python3
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controler.department import department_router
from controler.reports import router as reports_router
from controler.patient_controller import router as patients_router

app = FastAPI(
    title="MedPulse API",
    description="Hospital Database Management System",
    version="1.0.0"
)

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
app.include_router(reports_router)
app.include_router(patients_router)

@app.get("/")
async def root():
    return {"message": "Welcome to MedPulse API"}

if __name__ == "__main__":
    uvicorn.run("web.web:app", port=8080, reload=True)
