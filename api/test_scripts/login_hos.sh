#!/usr/bin/env bash

# ==============================
# Script to log in a hospital
# using HTTPie and HospitalLogin model
# ==============================

# Hospital login credentials
HOSPITAL_EMAIL="user@example.com"
PASSWORD="bode"

# Make POST request to login endpoint
http POST http://localhost:8080/login \
    hospital_email="$HOSPITAL_EMAIL" \
    password="$PASSWORD" \
    --json
