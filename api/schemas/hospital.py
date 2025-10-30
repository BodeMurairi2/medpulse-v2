from pydantic import BaseModel, EmailStr

class HospitalCreate(BaseModel):
    hospital_name: str
    hospital_email: EmailStr
    hospital_country: str
    hospital_city: str
    hospital_license: str
    password: str

class HospitalLogin(BaseModel):
    hospital_email: EmailStr
    password: str

