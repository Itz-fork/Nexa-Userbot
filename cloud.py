# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os

from pyrogram.types import Message
from gofile2 import Async_Gofile

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg
from config import Config


# Help
CMD_HELP.update(
    {
        "cloud": f"""
**Cloud Storages,**

  ✘ `gofile` - To upload telegram media to gofile.io

**Example:**

  ✘ `gofile`,
   ⤷ Reply to telegram media = `{Config.CMD_PREFIX}gofile` (Reply to a valid telegram media file)
      Tip: You can also send a description alongside with command!
"""
    }
)

mod_file = os.path.basename(__file__)


@nexaub_on_cmd(command="gofile", modlue=mod_file)
async def gofiles_up(_, message: Message):
    gofile_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_go_f = message.reply_to_message
    go_f_arg = get_arg(message)
    if not r_go_f:
        return await gofile_msg.edit("`Reply to a telegram media to upload it to Gofile.io!`")
    await gofile_msg.edit("`Download has started! This may take a while!`")
    dl_go_f = await r_go_f.download()
    desc = go_f_arg if go_f_arg else None
    # Gofile2 client
    go_client = Async_Gofile()
    await gofile_msg.edit("`Upload has started! This may take a while!`")
    upl_go_f = await go_client.upload(file=dl_go_f, description=desc)
    await gofile_msg.edit(f"**Successfully Uploaded!** \n\n**File Name:** `{upl_go_f['fileName']}` \n**Link:** {upl_go_f['downloadPage']}", disable_web_page_preview=True)