from configs.database import User
from utils.security import hash_password, verify_password
from utils.features import convertMongoDict, sendResponse, sendError
from utils.jwt import create_access_token, create_refresh_token
from utils.sendTokens import sendTokens
from configs.envConf import getEnv


# user register controller
# ----------------------------------------------------------
async def register_controller(body):
    try:
        isExist = await User.find_one({"email": body.email})
        if isExist:
            return sendError(403, "User already exist")
        # hash password
        # --------------
        body.password = hash_password(body.password)
        # create user in database
        # --------------
        user = await User.insert_one(body.dict())
        if not user.inserted_id:
            return sendError(500, "User creation failed")
        return sendTokens(
            201, "User Created Successfully", {"_id": str(user.inserted_id)}
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
async def logout_controller():
    try:
        response = sendResponse(200, "User Logged Out Successfully")
        response.delete_cookie(getEnv("ACCESS_TOKEN_NAME"))
        response.delete_cookie(getEnv("REFRESH_TOKEN_NAME"))
        return response
    except Exception as e:
        print("error in login controller", str(e))
        return sendError(500, "Internal Server Error", str(e))
