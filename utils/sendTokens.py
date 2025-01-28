from fastapi.responses import JSONResponse
from utils.features import sendError
from utils.jwt import create_access_token, create_refresh_token
from configs.envConf import config, getEnv
from configs.constants import accessTokenOptions, refreshTokenOptions


def sendTokens(statusCode: int, message: str, data: dict):
    try:
        if not data["_id"]:
            return sendError(500, "User creation failed")
        # create access and refresh token
        accessToken = create_access_token({"_id": data["_id"]})
        refreshToken = create_refresh_token({"_id": data["_id"]})
        # send access token and refresh token in user cookies
        if not accessToken or not refreshToken:
            return sendError(500, "Error in Authentication, login again")
        responseData = {"success": True, "message": message}
        response = JSONResponse(content=responseData, status_code=statusCode or 200)
        response.set_cookie(value=accessToken, **accessTokenOptions)
        response.set_cookie(value=refreshToken, **refreshTokenOptions)
        return response
    except Exception as e:
        print("error in sendTokens controller", str(e))
        return sendError(500, "Internal Server Error", str(e))
