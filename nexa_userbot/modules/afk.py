# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os

from pyrogram import filters
from pyrogram.types import Message
from datetime import datetime

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.nexaub_database.nexaub_db_afk import me_afk, get_afk, me_online
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r, nexaub_on_cf
from nexa_userbot.helpers.pyrogram_help import get_arg
from config import Config


# Help
CMD_HELP.update(
    {
        "afk": f"""
**Afk,**

  ✘ `afk` - To Activate Afk Module

**Example:**

  ✘ `afk`,
   ⤷ Send with reason = `{Config.CMD_PREFIX}afk This is the reason`
"""
    }
)

mod_file = os.path.basename(__file__)

# Check if afk
async def u_afk_bro(filter, client, message):
    if_afk = await get_afk()
    if if_afk:
        return True
    else:
        return False

# Creating a custom filter
ya_afk = filters.create(func=u_afk_bro, name="is_ya_afk")


@nexaub_on_cmd(command="afk", modlue=mod_file)
async def me_goin_oflin(_, message: Message):
    afk_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    afk_reason = get_arg(message)
    if not afk_reason:
        afk_reason = "I'm Busy For Now! Will Come Online Later :)"
    afk_time = datetime.now().replace(microsecond=0)
    await me_afk(afk_time=afk_time, afk_reason=afk_reason)
    await afk_msg.edit(f"**I'm Going AFK** \n\n**Reason:** `{afk_reason}`")

@nexaub_on_cf(
    ya_afk
    & (filters.mentioned | filters.private)
    & ~filters.me
    & ~filters.edited
    & filters.incoming)
async def me_afk_tho(_, message: Message):
    if not message:
        return
    if not message.from_user:
        return
    s_time, a_reason = await get_afk()
    now_time = datetime.now().replace(microsecond=0)
    afk_time = str((now_time - s_time))
    await message.reply(f"**I'm AFK** \n\n**Last Online:** `{afk_time}` \n**Reason:** `{a_reason}`")

@nexaub_on_cf(
    filters.me
    & filters.outgoing
    & ya_afk
)
async def back_online_bois(_, message: Message):
    s_time, a_reason = await get_afk()
    com_online = datetime.now().replace(microsecond=0)
    afk_time = str((com_online - s_time))
    await me_online()
    await e_or_r(nexaub_message=message, msg_text=f"**I'm No Longer AFK** \n\n**Afk Time:** `{afk_time}` \n**Reason:** `{a_reason}`")