# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
from time import time
from pyrogram import Client
from config import Config

# Configs
CMD_HELP = {}
StartTime = time()

NEXAUB = Client(
    api_hash=Config.API_HASH,
    api_id=Config.APP_ID,
    session_name=Config.PYRO_STR_SESSION,
    sleep_threshold=10
)