#!/usr/bin/env python3

from fastapi.routing import APIRouter

department_router = APIRouter(prefix="/department",
                              tags=["Departments"]
                              )

@department_router.get("/")
async def home():
    return {"message": "Department Home"}
