# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from nexa_userbot import NEXAUB
from nexa_userbot.core.nexaub_database.nexaub_db_conf import set_log_channel, get_log_channel
from config import Config


async def check_or_set_log_channel():
    try:
        log_channel_id = await get_log_channel()
        if log_channel_id:
            return [True, log_channel_id]
        else:
            log_channel = await NEXAUB.create_channel(title="Nexa Userbot Logs", description="Logs of your Nexa Userbot")
            welcome_to_nexaub = f"""
**Welcome to Nexa Userbot**
Thanks for trying Nexa Userbot. If you found any error, bug or even a Feature Request please report it at **@NexaUB_Support**

**⌲ Quick Start,**
If you don't know how to use this Userbot please send `{Config.CMD_PREFIX}help` in any chat. It'll show all plugins your userbot has. You can use those plugin names to get info about how to use it.


 **~ Nexa Userbot Authors**"""
            log_channel_id = log_channel.id
            await set_log_channel(log_channel_id)
            await NEXAUB.send_message(chat_id=log_channel_id, text=welcome_to_nexaub)
            return [True, log_channel_id]
    except Exception as e:
        print(f"Error \n\n{e} \n\nPlease check all variables and try again! \nReport this with logs at @NexaUB_Support if the problem persists!")
        exit()