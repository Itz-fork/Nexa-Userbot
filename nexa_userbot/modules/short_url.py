# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from pyrogram.types import Message
from nexa_userbot import CMD_HELP
from nexa_userbot.helpers.pyrogram_help import get_arg, extract_url_from_txt
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


# Supported url shortners list
SUPPORTED_URL_SHORTNERS = ["isgd", "dagd"]
# Headers for da.gd
dagd_header = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 6.0.1; Moto G (4)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Mobile Safari/537.36",
    "Accept": "text/html"
}


async def short_urls(url, shortner: str):
    async with ClientSession() as shortner_session:
        if shortner == "isgd":
            pasted_url = await shortner_session.post(f"https://is.gd/create.php?format=json&url={url}")
            json_data = await pasted_url.json()
            return [json_data['shorturl']]
        elif shortner == "dagd":
            async with shortner_session.get(f"https://da.gd/?url={url}", headers=dagd_header) as dagd_short:
                req_text = await dagd_short.text
                soup = BeautifulSoup(req_text, "html.parser")
                url_div = soup.find_all("div", attrs={"class": "constraint"})
                links = url_div[1].find("a", href=True)
                return await extract_url_from_txt(links)
        else:
            return ["https://github.com/Itz-fork/Nexa-Userbot"]


@nexaub_on_cmd(command="short", modlue=mod_file)
async def cutr_short(_, message: Message):
    short_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    replied_msg = message.reply_to_message
    args = get_arg(message)
    if replied_msg:
        base_txt = replied_msg.text
    elif args:
        base_txt = args
    else:
        return short_msg.edit("`Give some urls or reply to a message that contains urls to short!`")
    # Extracting urls from text
    urls = await extract_url_from_txt(base_txt)
    if not urls:
        return short_msg.edit("`Give some urls or reply to a message that contains urls to short!`")
    splitted_txt = base_txt.split(None)
    default_shtnr = "isgd"
    if len(splitted_txt) >= 2:
        if str(splitted_txt[1]) in SUPPORTED_URL_SHORTNERS:
            shortner = str(splitted_txt[1])
        else:
            shortner = default_shtnr
    else:
        shortner = default_shtnr
    # Short urls
    short_urls = "**Successfully Shortened the Url(s)** \n\n"
    for url in urls:
        shorted = await short_urls(url, shortner)
        short_urls += f"► **Shortened Url:** {shorted[0]} \n  **Original Url:** {url}"
    await short_msg.edit(short_urls, disable_web_page_preview=True)