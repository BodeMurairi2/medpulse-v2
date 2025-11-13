from pydantic import BaseModel, EmailStr

class PatientCreate(BaseModel):
    first_name : str
    second_name : str
    email : EmailStr
    phone_number : str
    date_of_birth : str
    password : str

class PatientOut(BaseModel):
    patient_id: int
    first_name: str
    second_name: str
    email: EmailStr
    phone_number: str

    class Config:
        orm_mode = True

class PatientLogin(BaseModel):
    email: EmailStr
    password: str

class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str
