from datetime import datetime, timedelta
from typing import Any, Optional
from jose import JWTError, jwt
from configs.envConf import getEnv

ALGORITHM = "HS256"


def create_jwt_token(data: dict, secret: str, expires_minutes: int) -> str:
    expires_minutes = expires_minutes
    expire = datetime.utcnow() + timedelta(seconds=expires_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, secret, algorithm=ALGORITHM)


# Function to decode the JWT token
def decode_token(token: str, secret_key: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, secret_key, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
