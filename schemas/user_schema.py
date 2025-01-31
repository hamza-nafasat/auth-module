from pydantic import BaseModel, EmailStr
from typing import Optional


class RegisterRequestSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class UpdateProfileSchema(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
