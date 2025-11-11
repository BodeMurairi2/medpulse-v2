#!/usr/bin/env bash

# Replace this with the token you got from /login
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N0b3JfaWQiOjIyLCJleHAiOjE3NjI4NzU1NDN9.VKjdA9yCCfpZnU-tCc3F1QmZwmUnHKt2x2YNPKRtizs"

# Make GET request to /patients
http GET http://localhost:8080/doctor_portal/patients/search/John%20Doe "Authorization: Bearer $TOKEN"
