from pydantic import BaseModel, EmailStr


class RegisterRequestSchema(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequestSchema(BaseModel):
    email: EmailStr
    password: str


class ResponseSchema(BaseModel):
    id: str
    name: str
    email: EmailStr
    is_active: bool
    is_verified: bool
