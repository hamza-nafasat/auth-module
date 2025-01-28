from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
import os
from configs.envConf import getEnv


client = AsyncIOMotorClient(getEnv("MONGO_URI"))
db = client[getEnv("DATABASE_NAME")]

# Collections


User = db["users"]
