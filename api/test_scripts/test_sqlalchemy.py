import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, inspect

load_dotenv()

# Replace with your actual database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL)

# Create inspector
inspector = inspect(engine)

# List columns of the table
columns = inspector.get_columns("prescriptions")
for column in columns:
    print(column["name"], column["type"])
