from utils.features import sendError
from fastapi import APIRouter, Depends, Request, Response
from schemas.user_schema import (
    LoginRequestSchema,
    RegisterRequestSchema,
    UpdateProfileSchema,
)
from middlewares.isAuthenticated import isAuthenticated
from controllers.user_controllers import (
    register_controller,
    login_controller,
    logout_controller,
    forgetPassword_controller,
    resetPassword_controller,
    getMyProfile_controller,
    updateProfile_controller,
)


router = APIRouter(prefix="/api/user", tags=["user"])


@router.post("/register")
async def register(request: RegisterRequestSchema):
    return await register_controller(RegisterRequestSchema(**request.dict()))


@router.post("/login")
async def login(request: LoginRequestSchema):
    return await login_controller(LoginRequestSchema(**request.dict()))


@router.post("/logout")
async def logout(response: Response, user: dict = Depends(isAuthenticated)):
    return await logout_controller(response, user)


@router.get("/forget-password")
async def forgetPassword(request: Request):
    return await forgetPassword_controller(request)


@router.patch("/reset-password")
async def resetPassword(request: Request):
    return await resetPassword_controller(request)


@router.get("/my-profile")
async def getMyProfile(user: dict = Depends(isAuthenticated)):
    return await getMyProfile_controller(user)


@router.patch("/my-profile")
async def updateMyProfile(
    req: UpdateProfileSchema, user: dict = Depends(isAuthenticated)
):
    return await updateProfile_controller(request, user)
