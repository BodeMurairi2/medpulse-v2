#!/usr/bin/env bash

# Doctor details
FIRST_NAME="Pascal"
LAST_NAME="Louis"
GENDER="Male"
DEPARTMENT="Cardiology"
PHONE_NUMBER="250795009077"
EMAIL="p.nsigo@alustudent.com"

# JWT token from hospital login
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJob3NwaXRhbF9pZCI6NiwiZXhwIjoxNzYzMDM2NTQ0fQ.7nLS8AdxvUS3CksXgmwIztKqEroRX4187ZVv1zih7YE"

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
