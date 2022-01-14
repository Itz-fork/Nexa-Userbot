# Copyright (c) 2021 Itz-fork
# Part of: Nexa Userbot

import os
import asyncio

from pyrogram.types import Message
from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from nexa_userbot.core.errors import Errors
from nexa_userbot.helpers.downloader import NexaDL
from nexa_userbot.helpers.up_to_tg import guess_and_send
from nexa_userbot.helpers.pyrogram_help import get_arg, extract_url_from_txt
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Downloader,**

  ✘ `dl` - To Download Files From Direct Links

**Example:**

  ✘ `dl`
   ⤷ Send with command = `{Config.CMD_PREFIX}dl http://www.ovh.net/files/100Mb.dat`


**Note:** `File size must be under 2GB (Telegram limits)`
""",
        f"{mod_name}_category": "tools"
    }
)


@nexaub.on_cmd(command=["dl"])
async def download_direct_links(_, message: Message):
  dl_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  args = get_arg(message)
  if r_msg:
    # Checks if the replied message has urls
    if not r_msg.text:
      return await dl_msg.edit("`Give a url or reply to a message that contains direct links to download it!`")
    urls = await extract_url_from_txt(r_msg.text)
    if not urls:
      return await dl_msg.edit("`Give a url or reply to a message that contains direct links to download it!`")
  elif args:
    urls = await extract_url_from_txt(args)
    if not urls:
      return await dl_msg.edit("`Give a url or reply to a message that contains direct links to download it!`")
  else:
    return await dl_msg.edit("`Give a url or reply to a message that contains direct links to download it!`")
  # Downloads the files from url
  dl_engine = NexaDL()
  file = await dl_engine.download(urls[0], message)
  await guess_and_send(file, message.chat.id, thumb_path="cache")