# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import asyncio
import logging

from pyrogram import idle
from nexa_userbot import NEXAUB
from nexa_userbot.modules import *
from nexa_userbot.core.startup_checks import check_or_set_log_channel, check_arq_api, download_plugins_in_channel, install_custom_plugins


async def main_startup():
    print("""
|| Nexa Userbot ||

Copyright (c) 2021 Itz-fork
"""
    )
    await NEXAUB.start()
    # Downloading and installing Custom Plugins
    logging.info("Downloading Custom Plugins...")
    await download_plugins_in_channel()
    logging.info("Installing Custom Plugins...")
    await install_custom_plugins()
    # Check or set log channel id
    logging.info("Checking Log Channel...")
    log_channel_id = await check_or_set_log_channel()
    # Check if arq api is available else it'll obtain a one
    logging.info("Checking ARQ API Key...")
    await check_arq_api()
    try:
        await NEXAUB.send_message(chat_id=log_channel_id[1], text="`Nexa Userbot is alive!`")
    except:
        logging.warn("There was an error while creating the LOG CHANNEL please add a one manually!")
    await idle()

loop = asyncio.get_event_loop()
loop.run_until_complete(main_startup())