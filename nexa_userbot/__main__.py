# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import asyncio

from pyrogram import idle
from nexa_userbot import NEXAUB
from nexa_userbot.modules import *
from nexa_userbot.core.startup_checks import check_or_set_log_channel, check_arq_api
from nexa_userbot.core.nexaub_database.nexaub_db_conf import get_log_channel
from config import Config


async def main_startup():
    print("""
|| Nexa Userbot ||

Copyright (c) 2021 Itz-fork
"""
    )
    await NEXAUB.start()
    await check_or_set_log_channel()
    await check_arq_api()
    log_channel_id = await get_log_channel()
    await NEXAUB.send_message(chat_id=log_channel_id, text="`Nexa Userbot is started!`")
    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(main_startup())