# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import asyncio
import time
import os

from pyrogram.types import Message
from pyrogram.errors import FloodWait

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from config import Config


# Help
CMD_HELP.update(
    {
        "owner": f"""
**Owner Stuff,**

  ✘ `block` - To Block a User
  ✘ `unblock` - To Unblock a Blocked User
  ✘ `kickme` - To Leave From a Chat
  ✘ `chats` - To Count your Chats (Unstable due to Floodwait Limits)

**Example:**

  ✘ `block`,
   ⤷ Reply to a message from user = `{Config.CMD_PREFIX}block`
   ⤷ Just send `{Config.CMD_PREFIX}block in PMs

  ✘ `unblock`
   ⤷ Send this command with user id to unblock = `{Config.CMD_PREFIX}unblock 1234567`
"""
    }
)

mod_file = os.path.basename(__file__)

# To Block a user
@nexaub_on_cmd(command="block", modlue=mod_file, no_sudos=True)
async def block_dumb(_, message: Message):
  shit_id = message.chat.id
  r_msg = message.reply_to_message
  gonna_block_u = await e_or_r(nexaub_message=message, msg_text="`Blocking User...`")
  try:
    if r_msg:
      await NEXAUB.block_user(r_msg.from_user.id)
      await gonna_block_u.edit("`Successfully Blocked This User`")
    else:
      await NEXAUB.block_user(shit_id)
      await gonna_block_u.edit("`Successfully Blocked This User`")
  except Exception as lol:
    await gonna_block_u.edit(f"**Error:** `{lol}`")

# To Unblock User That Already Blocked
@nexaub_on_cmd(command="unblock", modlue=mod_file, no_sudos=True)
async def unblock_boi(_, message: Message):
  good_bro = int(message.command[1])
  gonna_unblock_u = await e_or_r(nexaub_message=message, msg_text="`Unblocking User...`")
  try:
    await NEXAUB.unblock_user(good_bro)
    await gonna_unblock_u.edit(f"`Successfully Unblocked The User` \n**User ID:** `{good_bro}`")
  except Exception as lol:
    await gonna_unblock_u.edit(f"**Error:** `{lol}`")

# Leave From a Chat
@nexaub_on_cmd(command="kickme", modlue=mod_file, no_sudos=True, only_groups=True)
async def ubkickme(_, message: Message):
  i_go_away = await e_or_r(nexaub_message=message, msg_text="`Leaving This Chat...`")
  try:
    await NEXAUB.leave_chat(message.chat.id)
    await i_go_away.edit("`Successfully Leaved This Chat!`")
  except Exception as lol:
    await i_go_away.edit(f"**Error:** `{lol}`")

# To Get How Many Chats that you are in (PM's also counted)
@nexaub_on_cmd(command="chats", modlue=mod_file, no_sudos=True)
async def ubgetchats(_, message: Message):
  total=0
  getting_chats = await e_or_r(nexaub_message=message, msg_text="`Checking Your Chats, Hang On...`")
  async for dialog in NEXAUB.iter_dialogs():
    try:
      await NEXAUB.get_dialogs_count()
      total = total+1
      await getting_chats.edit(f"**Total Chats Counted:** `{total}`")
    except FloodWait as e:
      await time.sleep(e.x)