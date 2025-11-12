from pydantic import BaseModel, EmailStr

class PatientCreate(BaseModel):
    first_name : str
    last_name : str
    email : EmailStr
    phone : str
    dob : str
    password : str


class PatientOut(BaseModel):
    patient_id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True

class PatientLogin(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str