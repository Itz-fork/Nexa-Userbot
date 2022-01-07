# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os
import re

from pyrogram.types import Message
from io import BytesIO
from aiohttp import ClientSession

from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg, extract_url_from_txt
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Web Screenshot,**

  ✘ `webss` - To get a screenshot of given url

**Example:**

  ✘ `webss`,
   ⤷ Send command with url = `{Config.CMD_PREFIX}webss https://google.com`
   ⤷ Reply to a message = `{Config.CMD_PREFIX}webss`

  **Tips 💡,**
   ⤷ You can generate screenshots for multiple urls at the same time
   ⤷ You can capture the full page too. To do so use one of these commands instead of the default one.
    ⤷ `{Config.CMD_PREFIX}webssf`
    ⤷ `{Config.CMD_PREFIX}wssf`
""",
        f"{mod_name}_category": "tools"
    }
)


# Function to get screenshot of the page
async def gen_ss(url, full_page=False):
    if full_page:
        req_url = f"https://mini.s-shot.ru/1360x0/png/1024/Z100/?{url}"
    else:
        req_url = f"https://render-tron.appspot.com/screenshot/{url}"
    async with ClientSession() as webss_c:
        req = await webss_c.post(req_url)
        read_bytes = await req.read()
        screens = BytesIO(read_bytes)
    screens.name = f"Nexa-Userbot-webss_{url}.png"
    return screens

# Function to check type of the ss
async def is_full_page(cmd):
    if re.search(r'\bfwebss|wssf|fwss|webssf\b', cmd):
        full_page = True
    else:
        full_page = False
    return full_page

@nexaub.on_cmd(command=["webss", "wss", "fwss", "fwebss", "wssf", "webssf"])
async def gimme_a_damn_ss(_, message: Message):
    webss_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    w_args = get_arg(message)
    if r_msg:
        urls = await extract_url_from_txt(r_msg.text)
    elif w_args:
        urls = await extract_url_from_txt(w_args)
    else:
        return await webss_msg.edit("`Give me some urls or reply to a message that contains urls!`")
    if not urls:
        return await webss_msg.edit("`Give me some urls or reply to a message that contains urls!`")
    # Generating the screenshots
    ss_type = await is_full_page(message.text)
    for url in urls:
        if ss_type:
            webss = await gen_ss(url, True)
        else:
            webss = await gen_ss(url)
        await webss_msg.reply_document(webss, caption=f"**Scrrenshot Generated!** \n\n**Url:** {url}")
        webss.close()
    await webss_msg.delete()