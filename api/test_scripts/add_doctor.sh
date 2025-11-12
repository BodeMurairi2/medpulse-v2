#!/usr/bin/env bash

# Doctor details
FIRST_NAME="Bode"
LAST_NAME="Murairi"
GENDER="Male"
DEPARTMENT="Cardiology"
PHONE_NUMBER="250795020998"
EMAIL="b.murairi@alustudent.com"

# JWT token from hospital login
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJob3NwaXRhbF9pZCI6NiwiZXhwIjoxNzYyOTUwMDUwfQ.-gy5DP_s918M-7Fd03j72Zcc_R7wOwa5TAbOBGZIOvY"

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
