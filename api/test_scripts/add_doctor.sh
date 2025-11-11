#!/usr/bin/env bash

# Doctor details
FIRST_NAME="Laura"
LAST_NAME="Kwizera"
GENDER="Female"
DEPARTMENT="Cardiology"
PHONE_NUMBER="0789009924"
EMAIL="l.kwizera1@alustudent.com"
PASSWORD="laura"

# JWT token from hospital login
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJob3NwaXRhbF9pZCI6NiwiZXhwIjoxNzYyODcxMTkzfQ.F3fIV9YD0OzCHa5EW2xNHU2vF1J4cCIArojkUjwyq8Y"

# Make POST request with Authorization header
http POST http://localhost:8080/doctor/add \
    Authorization:"Bearer $TOKEN" \
    first_name="$FIRST_NAME" \
    last_name="$LAST_NAME" \
    gender="$GENDER" \
    department="$DEPARTMENT" \
    phone_number="$PHONE_NUMBER" \
    email="$EMAIL" \
    password="$PASSWORD" \
    --json
