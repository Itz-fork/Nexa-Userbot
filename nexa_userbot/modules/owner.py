# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import time
import os

from pyrogram.types import Message
from pyrogram.errors import FloodWait

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
      f"{mod_name}": f"""
**Owner Stuff,**

  ✘ `block` - To Block a User
  ✘ `unblock` - To Unblock a Blocked User
  ✘ `kickme` - To Leave From a Chat
  ✘ `chats` - To Count your Chats (Unstable due to Floodwait Limits)

**Example:**

  ✘ `block`,
   ⤷ Reply to a message from user = `{Config.CMD_PREFIX}block`
   ⤷ Just send `{Config.CMD_PREFIX}block` in PMs

  ✘ `unblock`
   ⤷ Send this command with user id to unblock = `{Config.CMD_PREFIX}unblock 1234567`
""",
        f"{mod_name}_category": "utils"
    }
)


# To Block a user
@nexaub.on_cmd(command=["block"], no_sudos=True)
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
@nexaub.on_cmd(command=["unblock"], no_sudos=True)
async def unblock_boi(_, message: Message):
  good_bro = int(message.command[1])
  gonna_unblock_u = await e_or_r(nexaub_message=message, msg_text="`Unblocking User...`")
  try:
    await NEXAUB.unblock_user(good_bro)
    await gonna_unblock_u.edit(f"`Successfully Unblocked The User` \n**User ID:** `{good_bro}`")
  except Exception as lol:
    await gonna_unblock_u.edit(f"**Error:** `{lol}`")

# Leave From a Chat
@nexaub.on_cmd(command=["kickme"], no_sudos=True, only_groups=True)
async def ubkickme(_, message: Message):
  i_go_away = await e_or_r(nexaub_message=message, msg_text="`Leaving This Chat...`")
  try:
    await NEXAUB.leave_chat(message.chat.id)
    await i_go_away.edit("`Successfully Leaved This Chat!`")
  except Exception as lol:
    await i_go_away.edit(f"**Error:** `{lol}`")

# To Get How Many Chats that you are in (PM's also counted)
async def count_chats():
  total=0
  async for dialog in NEXAUB.iter_dialogs():
    try:
      await NEXAUB.get_dialogs_count()
      total += 1
    except FloodWait as e:
      await time.sleep(e.x)
  return total

@nexaub.on_cmd(command=["chats"], no_sudos=True)
async def ubgetchats(_, message: Message):
  getting_chats = await e_or_r(nexaub_message=message, msg_text="`Checking Your Chats, Hang On...`")
  d_count = await count_chats()
  await getting_chats.edit(f"**Total Chats Counted:** `{d_count}`")