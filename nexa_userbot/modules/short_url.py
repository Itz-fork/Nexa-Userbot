# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

from httpx import AsyncClient
from bs4 import BeautifulSoup
from pyrogram.types import Message
from nexa_userbot import CMD_HELP
from nexa_userbot.helpers.pyrogram_help import get_arg, extract_url_from_txt
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Short Url,**

  ✘ `short` - To short long url using is.gd or da.gd

**Example:**

  ✘ Usage Format,
   ⤷ Send command with urls - `{Config.CMD_PREFIX}short [shortner_name] [links]`
   ⤷ Reply to a message - `{Config.CMD_PREFIX}short [shortner_name]`

   ✘ dagd Example,
    ⤷ Send command with url = `{Config.CMD_PREFIX}short dagd https://google.com`
    ⤷ Reply to a message = `{Config.CMD_PREFIX}short dagd`

  **Tip 💡,**
   ⤷ You can short multiple urls at the same time
""",
        f"{mod_name}_category": "tools"
    }
)


# Supported url shortners list
SUPPORTED_URL_SHORTNERS = ["isgd", "dagd"]
default_shtnr = "isgd"
# Headers for da.gd
dagd_header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
    "Accept": "text/html"
}

async def short_urls(url, shortner):
    async with AsyncClient() as shortner_session:
        if shortner == "isgd":
            isgd_short = await shortner_session.get(f"https://is.gd/create.php?format=json&url={url}")
            return [isgd_short.json()["shorturl"]]
        elif shortner == "dagd":
            dagd_short = await shortner_session.get(f"https://da.gd/?url={url}", headers=dagd_header)
            req_text = dagd_short.text
            soup = BeautifulSoup(req_text, "html.parser")
            url_div = soup.find_all("div", attrs={"class": "constraint"})
            links = url_div[1].find("a", href=True)
            return await extract_url_from_txt(links)
        else:
            isgd_short = await shortner_session.get(f"https://is.gd/create.php?format=json&url={url}")
            return [isgd_short.json()["shorturl"]]


@nexaub.on_cmd(command=["short"])
async def short_urls_func(_, message: Message):
    short_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    replied_msg = message.reply_to_message
    args = get_arg(message)
    if replied_msg:
        base_txt = replied_msg.text
    elif args:
        base_txt = args
    else:
        return await short_msg.edit("`Give some urls or reply to a message that contains urls to short!`")
    # Extracting urls from text
    urls = await extract_url_from_txt(base_txt)
    if not urls:
        return await short_msg.edit("`Give some urls or reply to a message that contains urls to short!`")
    splitted_txt = base_txt.split(" ")
    if splitted_txt[0] in SUPPORTED_URL_SHORTNERS:
        shortner = splitted_txt[0]
    else:
        shortner = default_shtnr
    # Short urls
    short_urls_txt = "**Successfully Shortened the Url(s)** \n\n"
    for url in urls:
        shorted_url = await short_urls(url, shortner)
        short_urls_txt += f"► **Shortened Url:** {shorted_url[0]} \n   **Original Url:** {url} \n"
    await short_msg.edit(short_urls_txt, disable_web_page_preview=True)