#!/bin/bash

# Replace these values with actual patient details
FIRST_NAME="Laura"
LAST_NAME="Kwizera"
EMAIL="user@example.com"
PHONE="1234567890"
DOB="2000-01-01"
PASSWORD="securepassword"

# Replace with your actual token
AUTH_TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N0b3JfaWQiOjIyLCJleHAiOjE3NjMwMzY2NTJ9.SKjsgp04eTGCYl1ArJNrfzlXO_L4sM1Pb4kFdaAQt0Q"

# API endpoint
URL="http://localhost:8080/patient/create"

# Make POST request using HTTPie with authorization
http POST "$URL" \
  "Authorization:Bearer $AUTH_TOKEN" \
  first_name="$FIRST_NAME" \
  last_name="$LAST_NAME" \
  email="$EMAIL" \
  phone="$PHONE" \
  dob="$DOB" \
  password="$PASSWORD"

