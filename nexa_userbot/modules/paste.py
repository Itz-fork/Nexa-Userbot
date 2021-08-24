# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Thanks to: Friday Userbot for idea / trick

import os
import requests

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from config import Config


# Help
CMD_HELP.update(
    {
        "paste": f"""
**Paste,**

  ✘ `paste` - To Paste Text to Hastebin

**Example:**

  ✘ `paste`,
   ⤷ Send text with command = `{Config.CMD_PREFIX}paste Paste this text`
   ⤷ Reply to a text file = `{Config.CMD_PREFIX}paste` (Reply to a text file)
   ⤷ Reply to a text message = `{Config.CMD_PREFIX}paste (Reply to a text message)
"""
    }
)

mod_file = os.path.basename(__file__)

@nexaub_on_cmd(command="paste", modlue=mod_file)
async def paste(client, message):
    paste_msg = await e_or_r(nexaub_message=message, msg_text="`Pasting to Hastebin...`")
    replied_msg = message.reply_to_message
    tex_t = get_arg(message)
    message_s = tex_t
    if not tex_t:
        if not replied_msg:
            await paste_msg.edit("`Reply To File or Send This Command With Text!`")
            return
        if not replied_msg.text:
            file = await replied_msg.download()
            m_list = open(file, "r").read()
            message_s = m_list
            print(message_s)
            os.remove(file)
        elif replied_msg.text:
            message_s = replied_msg.text
    haste_url = "https://hastebin.com/documents"
    haste_paste = requests.post(haste_url, data=message_s.encode('utf-8'), timeout=3)
    hp_data = haste_paste.json()
    url_key = hp_data['key']
    pasted_url = f"https://hastebin.com/{url_key}"
    pasted_url_raw = f"https://hastebin.com/raw/{url_key}"
    await paste_msg.edit(f"**Pasted to Hastebin** \n\n**Hastebin Url:** [Click here]({pasted_url}) \n**Raw Url:** [Click here]({pasted_url_raw})", disable_web_page_preview=True)