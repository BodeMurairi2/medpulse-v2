import bcrypt

def hash_password(password: str) -> str:
    if not isinstance(password, str):
        password = str(password)
    # Encode as UTF-8 and truncate to 72 bytes (bcrypt limit)
    password_bytes = password.encode('utf-8')[:72]
    # Generate a salt and hash the password
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    # Return as UTF-8 string
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    if not isinstance(password, str):
        password = str(password)
    password_bytes = password.encode('utf-8')[:72]
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)
