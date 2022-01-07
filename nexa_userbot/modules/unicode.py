# coding=utf-8
# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

from pyrogram.types import Message
from emoji import UNICODE_EMOJI
from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Unicode Detector,**

  ✘ `unicode` - To Check whether the replied message is unicode or not

**Example:**

  ✘ `unicode`,
   ⤷ Reply to a message = `{Config.CMD_PREFIX}unicode`
""",
        f"{mod_name}_category": "tools"
    }
)


@nexaub.on_cmd(command=["unicode", "uni"])
async def checks_unicode(_, message: Message):
    uni_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    if not r_msg:
        return await uni_msg.edit("`Reply to a text message!`")
    msg_text = r_msg.text
    if not msg_text:
        return await uni_msg.edit("`Reply to a text message!`")
    # Checking if the message have unicode characters
    uni_count = 0
    for char in list(msg_text):
        try:
            char.encode("ascii")
        except:
            if char in UNICODE_EMOJI["en"]:
                return
            uni_count += 1
    if uni_count == 0:
        await uni_msg.edit("`Non-Unicode Characters are included in this message!`")
    else:
        await uni_msg.edit(f"`{uni_count} Unicode Characters are included in this message!`")