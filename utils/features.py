from fastapi.responses import JSONResponse
from bson import ObjectId
from pydantic import BaseModel
from fastapi import Response
import json


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            # make v in object id
            print("v", v)
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


def setResponse(response: JSONResponse, statusCode: int, message: None, data=None):
    response.body
    response.status_code = statusCode
    if message:
        response.body["message"] = message
    if data:
        response.body["data"] = data
