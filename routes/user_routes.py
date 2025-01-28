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
async def register(request: LoginRequestSchema):
    return await login_controller(LoginRequestSchema(**request.dict()))


@router.get("/logout")
async def register():
    return await logout_controller()
