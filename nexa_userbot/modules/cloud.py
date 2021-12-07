# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os

from time import time
from pyrogram.types import Message
from gofile2 import Async_Gofile
from mega import Mega
from functools import partial
from asyncio import get_running_loop

from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg, progress_for_pyrogram
from nexa_userbot.core.nexaub_database.nexaub_db_conf import get_custom_var
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


# Gofile uploader
@nexaub_on_cmd(command="gofile", modlue=mod_file)
async def gofiles_up(_, message: Message):
    gofile_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_go_f = message.reply_to_message
    go_f_arg = get_arg(message)
    if not r_go_f:
        return await gofile_msg.edit("`Reply to a telegram media to upload it to Gofile.io!`")
    await gofile_msg.edit("`Download has started! This may take a while!`")
    start_time = time()
    dl_go_f = await r_go_f.download(progress=progress_for_pyrogram, progress_args=("**💫 Downloading... 💫** \n", gofile_msg, start_time))
    desc = go_f_arg if go_f_arg else None
    # Gofile2 client
    go_client = Async_Gofile()
    await gofile_msg.edit("`Upload has started! This may take a while!`")
    upl_go_f = await go_client.upload(file=dl_go_f, description=desc)
    await gofile_msg.edit(f"**Successfully Uploaded!** \n\n**File Name:** `{upl_go_f['fileName']}` \n**Link:** {upl_go_f['downloadPage']}", disable_web_page_preview=True)


# Mega.nz uploader
async def getMegaEmailandPass():
    m_email = await get_custom_var("MEGA_EMAIL")
    m_pass = await get_custom_var("MEGA_PASS")
    if not m_email or not m_pass:
        return None
    else:
        return [m_email, m_pass]

async def loginToMega(e_and_m):
    client = Mega().login(e_and_m[0], e_and_m[1])
    return client

async def UploadToMega(msg, file, mega):
    try:
        uploadfile = mega.upload(f"{file}", upstatusmsg=msg)
        public_link = mega.get_upload_link(uploadfile)
        # Editing the message with uploaded link
        await msg.edit(f"**Successfully Uploaded!** \n\n**Link:** {public_link}", disable_web_page_preview=True)
    except Exception as e:
        return await msg.edit(f"**Error:** \n`{e}`")

@nexaub_on_cmd(command="mega", modlue=mod_file)
async def meganz_upload(_, message: Message):
    meganz_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    # Mega.nz Email and Pass
    creds = await getMegaEmailandPass()
    if not creds:
        return await meganz_msg.edit(f"""
**No Mega.nz Email or Password Found!**
For functionality of this function you must set the `MEGA_EMAIL` and `MEGA_PASS` variables using `{Config.CMD_PREFIX}setvar` command.

**To do so,**

- `{Config.CMD_PREFIX}setvar` MEGA_EMAIL your_mega_email@your.domain
- `{Config.CMD_PREFIX}setvar` MEGA_PASS your_mega_password

**Note ⚠️:**
    These emails and passwords are just dummy ones. So replace them with your own email and password before running the command."""
        )
    else:
        r_msg = message.reply_to_message
        if not r_msg:
            return await meganz_msg.edit("`Reply to a telegram media first!`")
        # Downloading the file
        m_file = await r_msg.download()
        # Login to mega.nz account
        m_client = await loginToMega()
        loop = get_running_loop()
        await loop.run_in_executor(None, partial(UploadToMega, message, m_file, m_client))

@nexaub_on_cmd(command="test", modlue=mod_file)
async def testmsdffsd(_, message: Message):
    await e_or_r(nexaub_message=message, msg_text="`This is a test message`")