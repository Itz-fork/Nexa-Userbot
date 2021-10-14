# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import sys
import time
import time

from pyrogram import Client
from config import Config

# Helps
HELP = {}
CMD_HELP = {}
NEXAUB_VERSION = "v0.0.3"

StartTime = time.time()

NEXAUB = Client(
    api_hash=Config.API_HASH,
    api_id=Config.APP_ID,
    session_name=Config.PYRO_STR_SESSION
)
