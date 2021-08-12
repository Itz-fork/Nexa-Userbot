# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

class Config(object):
    APP_ID = os.environ.get("APP_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    # Pyrogram Session
    PYRO_STR_SESSION = os.environ.get("PYRO_STR_SESSION", "")
    # Telethon Session
    TELE_STR_SESSION = os.environ.get("TELE_STR_SESSION", "")
    CMD_PREFIX = os.environ.get("CMD_PREFIX", ".")