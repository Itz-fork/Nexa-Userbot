# Copyright (c) 2021 Itz-fork
# Part of: Nexa Userbot

import os
import asyncio

from pyrogram.types import Message
from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from nexa_userbot.core.errors import Errors
from nexa_userbot.helpers.downloader import Downloader
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

# Configs
PROGRESS_MSG = """
** » File Name:** `{name}`

** » Progress:** `{progress}`

** » Downloaded:** `{downloaded}`

** » Speed:** `{speed}`

** » ETA:** `{eta}`

** » Status:** `{status}`
"""

DETAILS_MSG = """
** » File Name:** `{name}`

** » Time Taken:** `{tt}`

** » Data hashes,**
   **› MD5:** `{md5}`
   **› SHA1:** `{sha1}`
   **› SHA256:** `{sha256}`
"""


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
  dl_engine = Downloader()
  dling_file = await dl_engine.download(urls[0])
  # Updating the message with process status
  while not (await dl_engine.isFinished(dling_file)):
    fdetails = await dl_engine.get_progress_details(dling_file)
    try:
      await dl_msg.edit(PROGRESS_MSG.format(
        name=os.path.basename(urls[0]),
        progress=fdetails["progress"],
        downloaded=fdetails["downloaded"],
        speed=fdetails["speed"],
        eta=fdetails["eta"],
        status=fdetails["status"]
        ))
    except:
      pass
    await asyncio.sleep(0.2)
  # Checks if the download was successful or not
  is_ok = await dl_engine.isSuccess(dling_file)
  if not is_ok:
    await dl_msg.edit("`Oops, Downloading process was unsuccessful!`")
    raise Errors.DownloadFailed("Download was unsuccessful")
  # Edit status message with file details
  dled_fdt = await dl_engine.get_downloaded_file_details(dling_file)
  await dl_msg.edit(DETAILS_MSG.format(
    name=os.path.basename(urls[0]),
    tt=dled_fdt["time"],
    md5=dled_fdt["md5"],
    sha1=dled_fdt["sha1"],
    sha256=dled_fdt["sha256"],
  ))
  # Sending file to the user
  await guess_and_send(dled_fdt["path"], message.chat.id, thumb_path="cache")