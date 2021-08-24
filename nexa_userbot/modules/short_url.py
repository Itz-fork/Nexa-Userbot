# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import requests
import os

from pyrogram import filters
from pyrogram.types import Message
from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from config import Config


# Help
CMD_HELP.update(
    {
        "short_url": f"""
**Short Url,**

  ✘ `short` - To short long url using is.gd's free api

**Example:**

  ✘ `short`,
   ⤷ Send command with url = `{Config.CMD_PREFIX}short https://google.com`
   ⤷ Reply to a url message = `{Config.CMD_PREFIX}short` (Reply to a message with url)
"""
    }
)

mod_file = os.path.basename(__file__)

def paste_isgd(url):
    main_url = f"https://is.gd/create.php?format=json&url={url}"
    pasted_url = requests.post(main_url)
    json_data = pasted_url.json()
    short_url = json_data['shorturl']
    return short_url

@nexaub_on_cmd(command="short", modlue=mod_file)
async def cutr_short(_, message: Message):
    replied_msg = message.reply_to_message
    short_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
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
