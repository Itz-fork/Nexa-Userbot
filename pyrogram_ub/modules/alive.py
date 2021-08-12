# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot

import time
from datetime import datetime
from pyrogram import filters, __version__ as pyrogram_version
from telethon import __version__ as telethon_version
from pyrogram.types import Message
from sys import version_info

from pyrogram_ub import NEXAUB, CMD_HELP, StartTime
from config import Config

CMD_HELP.update(
    {
        "alive": """
**Alive,**


  ✘ `alive` - To Check If Your Bot Alive or Not (Pyrogram)
  ✘ `ping_p` - To Check Ping of Pyrogram

  ✘ `talive` - To Check If Your Bot Alive or Not (Telethon)
  ✘ `ping_t` - To Check Ping of Telethon
"""
    }
)

# Get python version
python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
# Conver time in to readable format
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
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


@NEXAUB.on_message(filters.me & filters.command("alive", Config.CMD_PREFIX))
async def pyroalive(_, message: Message):
    uptime = get_readable_time((time.time() - StartTime))
    alive_bef_msg = await message.edit("`Processing...`")
    alive_pic = "cache/NEXAUB.png"
    alive_msg = f"""
    **Nexa UserBot is Alive**
    
    **Python Version:** `{python_version}`
    **Pyrogram Version:** `{pyrogram_version}`
    **Telethon Version:** `{telethon_version}`
    **Uptime: `{uptime}`**


**Deploy Your Own: @NexaBotsUpdates**"""
    await alive_bef_msg.delete()
    await message.reply_photo(alive_pic, caption=alive_msg)

@NEXAUB.on_message(filters.me & filters.command("ping_p", Config.CMD_PREFIX))
async def pingme(_, message: Message):
    start = datetime.now()
    end = datetime.now()
    ping_time = (end - start).microseconds / 1000
    ping_msg = await message.edit("`Processing...`")
    await ping_msg.edit(f"**Pong:** `{ping_time} ms`", disable_web_page_preview=True)
