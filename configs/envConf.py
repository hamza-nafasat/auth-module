from dotenv import load_dotenv
import os

load_dotenv()

config = {
    "MONGO_URI": os.getenv("MONGO_URI"),
    "DATABASE_NAME": os.getenv("DATABASE_NAME"),
    "FRONTEND_URL": os.getenv("FRONTEND_URL") or "http://localhost:3000",
    # access token
    "ACCESS_TOKEN_NAME": os.getenv("ACCESS_TOKEN_NAME"),
    "ACCESS_TOKEN_SECRET": os.getenv("ACCESS_TOKEN_SECRET"),
    "ACCESS_TOKEN_EXPIRE_SECONDS": os.getenv("ACCESS_TOKEN_EXPIRE_SECONDS"),
    # refresh token
    "REFRESH_TOKEN_NAME": os.getenv("REFRESH_TOKEN_NAME"),
    "REFRESH_TOKEN_SECRET": os.getenv("REFRESH_TOKEN_SECRET"),
    "REFRESH_TOKEN_EXPIRE_SECONDS": os.getenv("REFRESH_TOKEN_EXPIRE_SECONDS"),
    # reset token
    "RESET_TOKEN_NAME": os.getenv("RESET_TOKEN_NAME"),
    "RESET_TOKEN_SECRET": os.getenv("RESET_TOKEN_SECRET"),
    "RESET_TOKEN_EXPIRE_SECONDS": os.getenv("RESET_TOKEN_EXPIRE_SECONDS"),
    # mail
    "SMTP_SERVER": os.getenv("SMTP_SERVER"),
    "SMTP_PORT": os.getenv("SMTP_PORT"),
    "SMTP_USERNAME": os.getenv("SMTP_USERNAME"),
    "SMTP_PASSWORD": os.getenv("SMTP_PASSWORD"),
    "SENDER_EMAIL": os.getenv("SENDER_EMAIL"),
}


def getEnv(key: str):
    value = config.get(key)
    if value is None:
        raise KeyError(f"Environment variable '{key}' is missing")
    return value
