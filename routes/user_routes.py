from utils.features import sendError
from fastapi import APIRouter
from schemas.user_schema import RegisterRequestSchema, LoginRequestSchema
from controllers.user_controllers import (
    register_controller,
    login_controller,
    logout_controller,
)


router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register")
async def register(request: RegisterRequestSchema):
    return await register_controller(RegisterRequestSchema(**request.dict()))


@router.post("/login")
async def login(request: LoginRequestSchema):
    return await login_controller(LoginRequestSchema(**request.dict()))


@router.post("/logout")
async def logout():
    return await logout_controller()
