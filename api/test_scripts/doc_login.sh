#!/usr/bin/env bash

# Script to log in a doctor
# using HTTPie and DoctorLogin model

# Doctor credentials
EMAIL="l.kwizera1@alustudent.com"
PASSWORD="laura"

# Make POST request to doctor login endpoint
http POST http://localhost:8080/doctor_portal/login \
    email="$EMAIL" \
    password="$PASSWORD" \
    --json
