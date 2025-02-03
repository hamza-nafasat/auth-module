from fastapi import Request, HTTPException, Response
from configs.envConf import getEnv
from utils.jwt import decode_token, create_jwt_token
from configs.database import User
from configs.constants import accessTokenOptions
from bson import ObjectId
from utils.features import convertMongoDict


async def isAuthenticated(request: Request, response: Response):
    try:
        # Get access token from cookies   Decode access token and fetch user
        accessToken = request.cookies.get(getEnv("ACCESS_TOKEN_NAME"))
        if accessToken:
            accessPayload = decode_token(accessToken, getEnv("ACCESS_TOKEN_SECRET"))
            if not accessPayload:
                raise HTTPException(status_code=401, detail="Access token not decoded")
            user = await User.find_one({"_id": ObjectId(accessPayload["_id"])})
            if not user:
                raise HTTPException(
                    status_code=401, detail="User not found from access token"
                )
            return user
        # If access token is missing, check for refresh token   Decode refresh token and fetch user
        refreshToken = request.cookies.get(getEnv("REFRESH_TOKEN_NAME"))
        if not refreshToken:
            raise HTTPException(status_code=401, detail="Refresh token expired")
        refreshPayload = decode_token(refreshToken, getEnv("REFRESH_TOKEN_SECRET"))
        if not refreshPayload:
            raise HTTPException(status_code=401, detail="Refresh token not decoded")
        user = await User.find_one({"email": refreshPayload["email"]})
        if not user:
            raise HTTPException(
                status_code=401, detail="User not found from refresh token"
            )
        # Generate new access token
        accessToken = create_jwt_token(
            {"_id": str(user["_id"])},
            getEnv("ACCESS_TOKEN_SECRET"),
            int(getEnv("ACCESS_TOKEN_EXPIRE_SECONDS")),
        )
        response.set_cookie(value=accessToken, **accessTokenOptions)
        return user
    except Exception as e:
        print("Error in isAuthenticated middleware:", str(e))
        raise HTTPException(status_code=401, detail="Please Login Again")
