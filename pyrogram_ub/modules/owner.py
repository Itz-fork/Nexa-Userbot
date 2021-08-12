# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import asyncio
import time
import os

from pyrogram import filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from pyrogram_ub import NEXAUB, CMD_HELP
from config import Config

CMD_HELP.update(
    {
        "owner": """
**Owner Stuff,**


  ✘ `block` - To Block a User
  ✘ `unblock` - To Unblock a Blocked User
  ✘ `kickme` - To Leave From a Chat
  ✘ `chats` - To Count your Chats (Unstable due to Floodwait Limits)
"""
    }
)

# To Block a PM'ed User
@NEXAUB.on_message(filters.private & filters.command("block", Config.CMD_PREFIX) & filters.me & ~filters.edited)
async def block_dumb(_, message: Message):
  shit_id = message.chat.id
  gonna_block_u = await message.edit_text("`Blocking User...`")
  try:
    await NEXAUB.block_user(shit_id)
    await gonna_block_u.edit("`Successfully Blocked This User`")
  except Exception as lol:
    await gonna_block_u.edit(f"**Error:** `{lol}`")

# To Unblock User That Already Blocked
@NEXAUB.on_message(filters.command("unblock", Config.CMD_PREFIX) & filters.me & ~filters.edited)
async def unblock_boi(_, message: Message):
  good_bro = int(message.command[1])
  gonna_unblock_u = await message.edit_text("`Unblocking User...`")
  try:
    await NEXAUB.unblock_user(good_bro)
    await gonna_unblock_u.edit(f"`Successfully Unblocked The User` \n**User ID:** `{good_bro}`")
  except Exception as lol:
    await gonna_unblock_u.edit(f"**Error:** `{lol}`")

# Leave From a Chat
@NEXAUB.on_message(filters.command(["kickme", "leaveme"], Config.CMD_PREFIX) & filters.me & ~filters.edited)
async def ubkickme(_, message: Message):
  i_go_away = await message.edit_text("`Leaving This Chat...`")
  try:
    await NEXAUB.leave_chat(message.chat.id)
    await i_go_away.edit("`Successfully Leaved This Chat!`")
  except Exception as lol:
    await i_go_away.edit(f"**Error:** `{lol}`")

# To Get How Many Chats that you are in (PM's also counted)
@NEXAUB.on_message(filters.command("chats", [".", "/"]) & filters.me & ~filters.edited)
async def ubgetchats(_, message: Message):
  total=0
  getting_chats = await message.edit_text("`Checking Your Chats, Hang On...`")
  async for dialog in NEXAUB.iter_dialogs():
    try:
      await NEXAUB.get_dialogs_count()
      total = total+1
      await getting_chats.edit(f"**Total Chats Counted:** `{total}`")
    except FloodWait as e:
      await time.sleep(e.x)
