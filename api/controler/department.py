#!/usr/bin/env python3

from fastapi.routing import APIRouter
from fastapi import HTTPException, Query
from services.department import DepartmentService
from schemas.department import Department

department_router = APIRouter(prefix="/department",
                              tags=["Departments"]
                              )

service = DepartmentService()

@department_router.get("/")
async def home():
    return {"message": "Department Home"}

@department_router.get("/all")
async def get_departments_section(query: int | None = Query(default=None, description="Optional limit for departments")):
    """
    Get all departments or limit by index"""
    departments = service.get_departments()

    if query is None:
        return departments

    if query <= 0:
        raise HTTPException(status_code=400, detail="Query must be greater than 0")

    if query > len(departments):
        raise HTTPException(status_code=400, detail="Query exceeds number of departments available")

    return departments[:query]

@department_router.get("/search/{query}")
async def get_department(query:str):
    return service.get_department(department_name=query)

@department_router.post("/add")
async def add_department(department:Department):
    return service.add_department(department_data=department)

@department_router.put("/update/{department_name}")
async def update_department(department_name: str, department:Department):
    return service.edit_department(department_name=department_name, department_data=department)

@department_router.delete("/delete/{department_name}")
async def delete_department(department_name: str):
    return service.delete_department(department_name=department_name)
