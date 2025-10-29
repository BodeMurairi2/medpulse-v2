from fastapi import FastAPI
from api.web.hospital_routes import router as hospital_router

app = FastAPI()
app.include_router(hospital_router, prefix="/hospital")

