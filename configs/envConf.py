from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "MONGO_URI": os.getenv("MONGO_URI"),
    "DATABASE_NAME": os.getenv("DATABASE_NAME"),
    "ACCESS_TOKEN_NAME": os.getenv("ACCESS_TOKEN_NAME"),
    "ACCESS_TOKEN_SECRET_KEY": os.getenv("ACCESS_TOKEN_SECRET_KEY"),
    "ACCESS_TOKEN_EXPIRE_SECONDS": os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS"),
    "REFRESH_TOKEN_NAME": os.getenv("REFRESH_TOKEN_NAME"),
    "REFRESH_TOKEN_SECRET_KEY": os.getenv("REFRESH_TOKEN_SECRET_KEY"),
    "REFRESH_TOKEN_EXPIRE_SECONDS": os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS"),
}


def getEnv(key: str):
    value = config.get(key)
    if value is not None:
        return value
    else:
        raise KeyError(f"Environment variable '{key}' is missing")
