# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

class Config(object):
    APP_ID = os.environ.get("APP_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    # Pyrogram Session
    PYRO_STR_SESSION = os.environ.get("PYRO_STR_SESSION", "")
    CMD_PREFIX = os.environ.get("CMD_PREFIX", ".")
    MONGODB_URL = os.environ.get("MONGODB_URL")
    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY")