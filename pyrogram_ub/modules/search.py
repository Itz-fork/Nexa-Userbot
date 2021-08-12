# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Friday Userbot | DevsExpo

import re
import urllib
import urllib.parse
import requests

from pyrogram import filters
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from pyrogram_ub import NEXAUB, CMD_HELP
from pyrogram_ub.helpers.pyrogram_help import get_arg
from config import Config


CMD_HELP.update(
    {
        "search": """
**Search**


  ✘ `duck_s` - To Get Search Link In DuckDuckGo
  ✘ `google` - To Search In Google
"""
    }
)

@NEXAUB.on_message(filters.command("duck_s", Config.CMD_PREFIX) & filters.me)
async def duckduckg_s(client, message):
    pablo = await message.edit("`Searcing in DuckDuckGo...`")
    query = get_arg(message)
    if not query:
        await pablo.edit("`Give Something to Search!`")
        return
    sample_url = "https://duckduckgo.com/?q={}".format(query.replace(" ", "+"))
    link = sample_url.rstrip()
    await pablo.edit(f"**Query:** \n`{query}` \n\n**Result(s):** \n{link}")


@NEXAUB.on_message(filters.command("google", Config.CMD_PREFIX) & filters.me)
async def google_s(client, message):
    pablo = await message.edit("Searcing in Google...")
    query = get_arg(message)
    if not query:
        await pablo.edit("`Give Something to Search!`")
        return
    query = urllib.parse.quote_plus(query)
    number_result = 8
    ua = UserAgent()
    google_url = (
        "https://www.google.com/search?q=" + query + "&num=" + str(number_result)
    )
    response = requests.get(google_url, {"User-Agent": ua.random})
    soup = BeautifulSoup(response.text, "html.parser")
    result_div = soup.find_all("div", attrs={"class": "ZINbbc"})
    links = []
    titles = []
    descriptions = []
    for r in result_div:
        try:
            link = r.find("a", href=True)
            title = r.find("div", attrs={"class": "vvjwJb"}).get_text()
            description = r.find("div", attrs={"class": "s3v9rd"}).get_text()
            if link != "" and title != "" and description != "":
                links.append(link["href"])
                titles.append(title)
                descriptions.append(description)

        except:
            continue
    to_remove = []
    clean_links = []
    for i, l in enumerate(links):
        clean = re.search("\/url\?q\=(.*)\&sa", l)
        if clean is None:
            to_remove.append(i)
            continue
        clean_links.append(clean.group(1))
    for x in to_remove:
        del titles[x]
        del descriptions[x]
    msg = ""

    for tt, liek, d in zip(titles, clean_links, descriptions):
        msg += f"[{tt}]({liek})\n`{d}`\n\n"
    await pablo.edit(f"**Query:** \n`{query}` \n\n**Result(s):** \n{msg}")
