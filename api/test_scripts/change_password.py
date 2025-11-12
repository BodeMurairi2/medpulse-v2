#!/usr/bin/env python3

import requests

# Backend URL
URL = "http://localhost:8080/doctor_portal/change_password"

# JWT token of the logged-in doctor
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N0b3JfaWQiOjIyLCJleHAiOjE3NjI5NDQwNTF9.T3UYmm4D0e5TyDb-t32XjJjC-iazLkQ9_6VeMS9-NgU"

# Headers including authorization
headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# Request body
data = {
    "old_password": "laura",
    "new_password": "laura2"
}

# Make POST request
response = requests.post(URL, headers=headers, json=data)

# Check response
if response.status_code == 200:
    print("Password changed successfully")
else:
    print(f"Failed to change password: {response.status_code} {response.text}")
