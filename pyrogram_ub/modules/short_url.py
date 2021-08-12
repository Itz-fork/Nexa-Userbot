# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import requests

from pyrogram import filters
from pyrogram.types import Message
from pyrogram_ub import NEXAUB, CMD_HELP
from pyrogram_ub.helpers.pyrogram_help import get_arg
from config import Config

CMD_HELP.update(
    {
        "short_url": """
**Short Url,**

  ✘ `short` - To short long url using is.gd's free api
"""
    }
)

def paste_isgd(url):
    main_url = f"https://is.gd/create.php?format=json&url={url}"
    pasted_url = requests.post(main_url)
    json_data = pasted_url.json()
    short_url = json_data['shorturl']
    return short_url

@NEXAUB.on_message(filters.command("short", Config.CMD_PREFIX) & filters.me & ~filters.edited)
async def cutr_short(_, message: Message):
    replied_msg = message.reply_to_message
    short_msg = await message.edit("`Processing...`")
    if replied_msg:
        to_short = replied_msg.text
    elif not replied_msg:
        try:
            to_short = get_arg(message)
        except Exception as e:
            await short_msg.edit(f"**Error:** `{e}`")
            return
    shoterned_url = paste_isgd(to_short)
    try:
        print(shoterned_url)
        await short_msg.edit(f"**Successfully Shortened the Url** \n\n**Shortened Url:** {shoterned_url} \n**Original Url:** {to_short}", disable_web_page_preview=True)
    except Exception as e:
        await short_msg.edit(f"**Error:** `{e}`")
