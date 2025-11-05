#!/usr/bin/env python3

from fastapi.routing import APIRouter
from fastapi import HTTPException, Query

router = APIRouter(prefix="/patientList",
                   tags=["ListOfPatients"])


@router.get("/")
async def patients():
    return {"message":"Welcome to patients list page"}

