# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot

import sys
import time
import requests

from datetime import datetime
from io import BytesIO
from PIL import Image
from pyrogram import __version__ as pyrogram_version
from telethon import __version__ as telethon_version
from telethon import events, TelegramClient
from telethon_ub import NEXAUB, StartTime
from config import Config

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

python_version = f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"


@NEXAUB.on(events.NewMessage(outgoing=True, pattern=f"{Config.CMD_PREFIX}talive"))
async def tele_alive(event):
    start = datetime.now()
    end = datetime.now()
    (end - start).microseconds / 1000
    uptime = get_readable_time((time.time() - StartTime))
    alive_bef_msg = await event.edit("`Processing...`")
    alive_pic = "cache/NEXAUB.png"
    alive_msg = f"""
    **Nexa UserBot is Alive**
    
    **Python Version:** `{python_version}`
    **Pyrogram Version:** `{pyrogram_version}`
    **Telethon Version:** `{telethon_version}`
    **Uptime: `{uptime}`**
    
    
    **Deploy Your Own: @NexaBotsUpdates**"""
    await alive_bef_msg.delete()
    await NEXAUB.send_file(event.chat_id, alive_pic, caption=alive_msg)

@NEXAUB.on(events.NewMessage(outgoing=True, pattern=f"{Config.CMD_PREFIX}ping_t"))
async def _(event):
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    alive_msg = await event.edit("`Processing...`")
    await alive_msg.edit(f"**Pong:** `{ms} ms`", parse_mode="md")
