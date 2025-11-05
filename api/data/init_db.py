from .models import Base
from .database import engine
import os
from dotenv import load_dotenv

load_dotenv()

def create_tables():
    """Create all tables in the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()