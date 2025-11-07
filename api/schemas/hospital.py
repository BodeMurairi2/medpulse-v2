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

class DoctorCreate(BaseModel):
    first_name: str
    last_name: str
    gender: str | None = None
    department: str | None = None
    phone_number: str | None = None
    email: EmailStr
    password: str 

