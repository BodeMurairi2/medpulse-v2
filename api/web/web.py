from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from data.database import Base, engine
from controler.department import department_router
from controler.view_doctor import router as doctor_view_router
from controler.hospital_routes import router as hospital_router
from controler.doctor_portal import doctor_portal_router
from controler.doctor_routes import router as doctor_router
from controler.patient_controller import router as patient_router
from web.patient_routes import router as patient_router_auth
from web.patient_routes_create import router as patient_router_create
import uvicorn
from sqlalchemy.exc import OperationalError
from time import sleep

load_dotenv()

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

# Include routers once
app.include_router(department_router)
app.include_router(doctor_view_router)
app.include_router(hospital_router)
app.include_router(doctor_portal_router)
app.include_router(doctor_router)
app.include_router(patient_router)
app.include_router(patient_router_auth)
app.include_router(patient_router_create)

# Create tables on startup, retry until DB is ready
@app.on_event("startup")
def on_startup():
    connected = False
    while not connected:
        try:
            Base.metadata.create_all(bind=engine)
            connected = True
            print("All tables created successfully")
        except OperationalError:
            print("Database not ready yet, retrying in 2 seconds...")
            sleep(4)

@app.get("/")
async def root():
    return {"message": "Welcome to MedPulse API"}

if __name__ == "__main__":
    uvicorn.run("web.web:app", host="0.0.0.0", port=8080, reload=True)
