# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot

import time
from datetime import datetime
from telethon import TelegramClient
from telethon.sessions import StringSession
from config import Config

StartTime = time.time()
NEXAUB = TelegramClient(StringSession(Config.TELE_STR_SESSION), api_id=Config.APP_ID, api_hash=Config.API_HASH)