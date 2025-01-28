from fastapi.responses import JSONResponse
from bson import ObjectId
from pydantic import BaseModel


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)


# convert mongodb _id ObjectId to string
# ------------------------------------------------
def convertMongoDict(obj):
    obj["_id"] = str(obj["_id"])
    return obj


def convertMongoList(list):
    for i in range(len(list)):
        list[i] = convertMongoDict(list[i])
    return list


# functions to send response in success or error
# ------------------------------------------------
def sendResponse(statusCode: int, message: str, data=None):
    response = {"success": True, "message": message}
    if data:
        response["data"] = data
    return JSONResponse(
        content=response,
        status_code=statusCode or 200,
    )


def sendError(statusCode: int, message: str, error=None):
    response = {"success": False, "message": message}
    if error:
        response["error"] = error
    return JSONResponse(
        content=response,
        status_code=statusCode or 500,
    )
