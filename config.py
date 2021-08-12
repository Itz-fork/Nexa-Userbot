# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os
import heroku3

# Credits: Friday Userbot
def fetch_heroku_git_url(api_key, app_name):
    if not api_key:
        return None
    if not app_name:
        return None
    heroku = heroku3.from_key(api_key)
    try:
        heroku_applications = heroku.apps()
    except:
        return None
    heroku_app = None
    for app in heroku_applications:
        if app.name == app_name:
            heroku_app = app
            break
    if not heroku_app:
        return None
    return heroku_app.git_url.replace("https://", "https://api:" + api_key + "@")

class Config(object):
    APP_ID = os.environ.get("APP_ID", "")
    API_HASH = os.environ.get("API_HASH", "")
    # Pyrogram Session
    PYRO_STR_SESSION = os.environ.get("PYRO_STR_SESSION", "")
    # Telethon Session
    TELE_STR_SESSION = os.environ.get("TELE_STR_SESSION", "")
    CMD_PREFIX = os.environ.get("CMD_PREFIX", ".")

    HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME", None)
    HEROKU_API_KEY = os.environ.get("HEROKU_API_KEY", None)
    UPSTREAM_REPO = os.environ.get("UPSTREAM_REPO", "https://github.com/Itz-fork/Nexa-Userbot")
    HEROKU_URL = fetch_heroku_git_url(HEROKU_API_KEY, HEROKU_APP_NAME)
