#!/usr/bin/env python3
import os
from dotenv import load_dotenv
from sqlalchemy import or_, and_, func
from rapidfuzz import fuzz

load_dotenv()

def search_user(user_name:str, database, session):
    """Optimized search for patients using POST."""
    name_parts = user_name.split()
    filters = [
        or_(
            func.trim(database.first_name).ilike(f"%{part}%"),
            func.trim(database.last_name).ilike(f"%{part}%")
        )
        for part in name_parts
    ]
    query_filter = and_(*filters)

    candidates = session.query(database).filter(query_filter).all()

    # Optional fuzzy matching
    threshold = int(os.getenv("threshold"))
    users = [
        p for p in candidates
        if fuzz.partial_ratio(
            user_name.lower(),
            f"{p.first_name} {p.last_name}".lower()
        ) >= threshold
    ]
    return users or []

if __name__ == "__main__":
    search_user(user_name, database, session)
