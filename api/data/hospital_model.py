#!/usr/bin/env python3
from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

class Hospital(Base):
    __tablename__ = "hospitals"
    hospital_id = Column(Integer, primary_key=True, autoincrement=True)
    hospital_name = Column(String)
    hospital_email = Column(String)
    hospital_country = Column(String)
    hospital_city = Column(String)
    hospital_license = Column(String)
    password_hash = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
