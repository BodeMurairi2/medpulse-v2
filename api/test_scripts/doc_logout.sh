#!/usr/bin/env bash

# Doctor logout script using HTTPie

# JWT token obtained from login
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkb2N0b3JfaWQiOjIyLCJleHAiOjE3NjI4NzE3OTN9.ZblIJ5aLJ4X4IK1qfMtfCwsyEWzP7o2PUOFh029X2ds"

# Make POST request to logout endpoint with Authorization header
http POST http://localhost:8080/doctor_portal/logout \
    Authorization:"Bearer $TOKEN" \
    --json
