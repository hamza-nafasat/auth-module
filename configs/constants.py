from configs.envConf import getEnv

accessTokenOptions = {
    "key": getEnv("ACCESS_TOKEN_NAME"),
    "httponly": True,
    "secure": True,
    "samesite": "Lax",
    "max_age": int(getEnv("ACCESS_TOKEN_EXPIRE_SECONDS")),
}

refreshTokenOptions = {
    "key": getEnv("REFRESH_TOKEN_NAME"),
    "httponly": True,
    "secure": True,
    "samesite": "Lax",
    "max_age": int(getEnv("REFRESH_TOKEN_EXPIRE_SECONDS")),
}
