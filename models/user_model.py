from bson import ObjectId
from typing import Optional
from pydantic import BaseModel, EmailStr
from utils.features import PyObjectId


class UserModel(BaseModel):
    id: PyObjectId = None
    full_name: str
    email: EmailStr
    password: str
    is_active: bool = True
    is_verified: bool = False
