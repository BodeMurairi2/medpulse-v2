#!/usr/bin/env bash

# Replace this with the token you got from /login
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N0b3JfaWQiOjIyLCJleHAiOjE3NjMwOTg5NjV9.DZ6_6gLHVXXzQbD9GIz7LKUeMAYoMNudDfJWSRRu6jU"

# Make GET request to /patients
http GET http://localhost:8080/doctor_portal/patients "Authorization: Bearer $TOKEN"
