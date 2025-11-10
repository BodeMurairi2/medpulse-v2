from api.data.database import engine
from api.data.models import Base

print("Creating tables in the database...")
Base.metadata.create_all(bind=engine)
print("All tables created successfully!")
