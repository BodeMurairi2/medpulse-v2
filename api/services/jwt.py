import jwt
from datetime import datetime, timedelta
from decouple import config
from services.token_blacklist import is_token_blacklisted

JWT_SECRET = config("SECRET")
JWT_ALGORITHM = config("ALGORITHM")
MINS_TO_EXPIRE = 15

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=MINS_TO_EXPIRE))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        if is_token_blacklisted(token):
            return None
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
