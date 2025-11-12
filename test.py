from sqlalchemy import create_engine
from api.data.database import Base, DATABASE_URL
from api.data import hospital_model

engine = create_engine(DATABASE_URL)

Base.metadata.drop_all(bind=engine)
print("All tables dropped")

Base.metadata.create_all(bind=engine)
print("All tables created successfully.")
