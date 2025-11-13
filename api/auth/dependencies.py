#!/usr/bin/env python3
from fastapi import Header, HTTPException, status
from services.jwt import decode_access_token

def get_current_hospital(authorization: str = Header(...)):
    if not authorization or " " not in authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing or invalid"
        )

    scheme, token = authorization.split(" ", 1)
    if scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header must start with Bearer"
        )

    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )

    return payload.get("hospital_id")
