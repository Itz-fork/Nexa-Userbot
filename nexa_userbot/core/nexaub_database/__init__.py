# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from motor.motor_asyncio import AsyncIOMotorClient
from config import Config

mongodb = AsyncIOMotorClient(Config.MONGODB_URL)
nexa_mongodb = mongodb["NEXAUB"]