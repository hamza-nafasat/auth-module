from datetime import datetime, timedelta
from typing import Any, Optional
from jose import JWTError, jwt
from configs.envConf import getEnv

ALGORITHM = "HS256"
ACCESS_SECRET = getEnv("ACCESS_TOKEN_SECRET")
REFRESH_SECRET = getEnv("REFRESH_TOKEN_SECRET")
ACCESS_TIME = int(getEnv("ACCESS_TOKEN_EXPIRE_SECONDS"))
REFRESH_TIME = int(getEnv("REFRESH_TOKEN_EXPIRE_SECONDS"))


# Function to create an access token
def create_access_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    expires_minutes = expires_minutes or ACCESS_TIME
    expire = datetime.utcnow() + timedelta(seconds=expires_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, ACCESS_SECRET, algorithm=ALGORITHM)


# Function to create a refresh token
def create_refresh_token(data: dict, expires_minutes: Optional[int] = None) -> str:
    expires_minutes = expires_minutes or REFRESH_TIME
    expire = datetime.utcnow() + timedelta(seconds=expires_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, REFRESH_SECRET, algorithm=ALGORITHM)


# Function to decode the JWT token
def decode_token(token: str, secret_key: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
