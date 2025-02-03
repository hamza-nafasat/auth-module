from configs.database import User
from utils.security import hash_password, verify_password
from utils.features import convertMongoDict, sendResponse, sendError, setResponse
from utils.jwt import create_jwt_token, decode_token
from utils.sendTokens import sendTokens
from configs.envConf import getEnv
from fastapi import Response, Request
from fastapi.responses import JSONResponse
from bson import ObjectId
from utils.sendMail import sendMail


# user register controller
# ----------------------------------------------------------
async def register_controller(body):
    try:
        isExist = await User.find_one({"email": body.email})
        if isExist:
            return sendError(403, "User already exist")
        # hash password and create user in database
        body.password = hash_password(body.password)
        user = await User.insert_one(body.dict())
        if not user.inserted_id:
            return sendError(500, "User creation failed")
        return sendTokens(
            201,
            "User Created Successfully",
            {"_id": str(user.inserted_id), "email": body.email},
        )
    except Exception as e:
        print("error in register controller", str(e))
        return sendError(500, "Internal Server Error", str(e))


# user login controller
# ----------------------------------------------------------
async def login_controller(body):
    try:
        user = await User.find_one({"email": body.email})
        if not user:
            return sendError(404, "You need to register first")
        if not verify_password(body.password, user["password"]):
            return sendError(401, "Invalid credentials")
        return sendTokens(200, "User Logged In Successfully", convertMongoDict(user))
    except Exception as e:
        print("error in login controller", str(e))
        return sendError(500, "Internal Server Error", str(e))


# user logout controller
# ----------------------------------------------------------
async def logout_controller(response: Response, user: dict):
    try:
        response.delete_cookie(getEnv("ACCESS_TOKEN_NAME"))
        response.delete_cookie(getEnv("REFRESH_TOKEN_NAME"))
        return {"success": True, "message": "User Logged Out Successfully"}
    except Exception as e:
        print("error in logout controller", str(e))
        return sendError(500, "Internal Server Error", str(e))


# forget password
# ----------------------------------------------------------
async def forgetPassword_controller(request):
    try:
        query = request.query_params
        email = query.get("email")
        if not email:
            return sendError(400, "Email is required")
        # if get email check user exist for this email or not
        user = await User.find_one({"email": email})
        if not user:
            return sendError(404, "User not found")
        # if user find then create verification token and send on user email with nodemailer
        verificationToken = create_jwt_token(
            {"email": email},
            getEnv("RESET_TOKEN_SECRET"),
            int(getEnv("RESET_TOKEN_EXPIRE_SECONDS")),
        )
        resetLink = f"{getEnv('FRONTEND_URL')}/reset-password?token={verificationToken}"
        isMailSent = await sendMail(
            email,
            "Reset Password",
            f"Please click on the link to reset your password: {resetLink}",
        )
        if not isMailSent:
            return sendError(500, "Error in sending mail")
        return sendResponse(200, "Email sent successfully", verificationToken)
    except Exception as e:
        print("error in forgetPassword controller", str(e))
        return sendError(500, "Internal Server Error", str(e))


# reset password
# ----------------------------------------------------------
async def resetPassword_controller(request):
    try:
        query = request.query_params
        newPassword = query.get("newPassword")
        token = query.get("token")
        # validation
        if not newPassword:
            return sendError(400, "New Password is required")
        if not token:
            return sendError(400, "Token is required")
        # if get token check user exist for this token or not after decoding token
        decode = decode_token(token, getEnv("RESET_TOKEN_SECRET"))
        print("decode_token", decode)
        user = await User.find_one({"email": decode["email"]})
        if not user:
            return sendError(404, "User not found")
        # if user find then update password in database
        user["password"] = hash_password(newPassword)
        await User.update_one({"_id": user["_id"]}, {"$set": user})
        return sendResponse(200, "Password reset successfully")
    except Exception as e:
        print("error in resetPassword controller", str(e))
        return sendError(500, "Internal Server Error", str(e))


# get my profile controller
# ----------------------------------------------------------
async def getMyProfile_controller(user: dict):
    try:
        return {"success": True, "data": convertMongoDict(user)}
    except Exception as e:
        print("error in getMyProfile controller", str(e))
        return sendError(500, "Internal Server Error", str(e))


# get my profile controller
# ----------------------------------------------------------
async def updateProfile_controller(data, user: dict):
    try:
        user_id = user["_id"]
        dataForUpdate = {}
        if data.name:
            dataForUpdate["name"] = data.name
        if data.email:
            dataForUpdate["email"] = data.email
        if not dataForUpdate:
            return sendError(400, "At least one field is required")
        await User.update_one({"_id": user_id}, {"$set": dataForUpdate})
        return sendResponse(200, "Profile Updated Successfully")
    except Exception as e:
        print("error in updateProfile controller", str(e))
        return sendError(500, "Internal Server Error", str(e))
