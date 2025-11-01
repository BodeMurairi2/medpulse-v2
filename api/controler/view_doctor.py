#!/usr/bin/env python3

from fastapi.routing import APIRouter
from fastapi import HTTPException, Query
from services.view_doctor import View_doctor

router = APIRouter(prefix="/doctorsList",
                              tags=["ListDoctors"]
                              )

service = View_doctor()

@router.get("/")
async def doctors_home():
    return {"message":"Welcome to Doctors page"}

@router.get("/list")
async def get_doctors_list():
    return service.get_doctors()

@router.get("/list/{doctor_name}")
async def get_doctor(doctor_name:str):
    return service.get_doctor(doctor_name=doctor_name)

@router.get("/list/stats/{doctor_name}")
async def get_doctor_statistic(doctor_name):
    return service.get_doctor_statistics(doctor_name=doctor_name)
