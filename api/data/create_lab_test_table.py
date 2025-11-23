#!/usr/bin/env python3
from sqlalchemy import inspect
from .database import Base, engine
from .hospital_model import LabTestFile

# Inspect the database
inspector = inspect(engine)
if 'lab_test_files' in inspector.get_table_names():
    print("Table 'lab_test_files' already exists in the database.")
else:
    # Create the table
    LabTestFile.__table__.create(bind=engine)
    print("Table 'lab_test_files' created successfully.")
