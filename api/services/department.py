#!/usr/bin/env python3

from fastapi import HTTPException
from schemas.department import Department


class DepartmentService:
    """Service class for Department Operations"""

    def __init__(self):
        self.departments = [
            {
                "department_name": "Cardiology",
                "department_description": "Handles all heart-related medical issues and treatments.",
                "department_email": "cardiologysaintetienne@admin.com",
                "phone": "18005551234",
                "location": "Building A, Floor 3",
                "head_doctor": "Dr. John Smith",
                "number_staff": 25,
                "status": True
            },
            {
                "department_name": "Neurology",
                "department_description": "Specializes in disorders of the nervous system including the brain and spinal cord.",
                "department_email": "bodemurairi2@gmail.com",
                "phone": "18005554321",
                "location": "Building B, Floor 2",
                "head_doctor": "Dr. Jane Doe",
                "number_staff": 30,
                "status": True
            },
            {
                "department_name": "Pediatrics",
                "department_description": "Provides medical care for infants, children, and adolescents.",
                "department_email": "bodemurairi2@gmail.com",
                "phone": "18005559876",
                "location": "Building C, Floor 1",
                "head_doctor": "Dr. Emily White",
                "number_staff": 20,
                "status": True
            }
        ]

    def _find_department(self, department_name: str) -> dict:
        """Find a department by name (case-insensitive)."""
        for department in self.departments:
            if department_name.lower() == department["department_name"].lower():
                return department
        raise HTTPException(status_code=404, detail=f"Department '{department_name}' not found")

    def get_departments(self) -> list[Department]:
        """Get all departments."""
        return self.departments

    def search_departments(self, query: str) -> list[Department]:
        """Search departments by partial name (case-insensitive)."""
        results = [
            dept for dept in self.departments
            if query.lower() in dept["department_name"].lower()
        ]
        if not results:
            raise HTTPException(status_code=404, detail="No departments found matching the query")
        return results

    def get_department(self, department_name: str) -> Department:
        """Get a single department by name."""
        return self._find_department(department_name)

    def add_department(self, department_data: Department) -> Department:
        """Add a new department."""
        if any(d["department_name"].lower() == department_data.department_name.lower() for d in self.departments):
            raise HTTPException(status_code=400, detail="Department already exists")
        self.departments.append(department_data.model_dump())
        return department_data

    def edit_department(self, department_data: Department, department_name: str) -> Department:
        """Edit an existing department."""
        department = self._find_department(department_name)
        department.update(department_data.model_dump())
        return department

    def delete_department(self, department_name: str) -> dict:
        """Deactivate a department"""
        department = self._find_department(department_name)
        department["status"] = False
        return {"detail": f"Department '{department_name}' marked as inactive"}
