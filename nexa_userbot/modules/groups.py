# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os
import asyncio

from . import nexaub_devs
from pyrogram.types import Message
from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg
from config import Config


# Help
mod_file = os.path.basename(__file__)
mod_name = mod_file[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Group Tools,**

  ✘ `purge` - To purge messages in a chat
  ✘ `ban` - To ban a member in a chat
  ✘ `kick` - To kick a member in a chat
  ✘ `unban` - To unban a member in a chat
  ✘ `pin` - To pin a message in a chat
  ✘ `unpin` - To unpin a message or messages in a chat

**Example:**

  ✘ `purge`,
   ⤷ reply to a message = `{Config.CMD_PREFIX}purge`
  
  ✘ `ban`,
   ⤷ reply to a message (ban) = `{Config.CMD_PREFIX}ban`
   ⤷ send with user id (ban) = `{Config.CMD_PREFIX}ban 1234567`

  ✘ `unban`,
   ⤷ Same logic and arguments as the ban

  ✘ `kick`,
   ⤷ Same logic and arguments as the ban

   **Tip 💡,**
    ⤷ You can also pass a custom kick time in sec. - `{Config.CMD_PREFIX}kick 1234567 4`
  
  ✘ `pin`,
   ⤷ reply to a message = `{Config.CMD_PREFIX}pin`
   ⤷ pin with no notification = `{Config.CMD_PREFIX}pin -dn`
  
  ✘ `unpin`,
   ⤷ reply to a message = `{Config.CMD_PREFIX}unpin`
   ⤷ unpin all messages = `{Config.CMD_PREFIX}unpin -all`
""",
        f"{mod_name}_category": "utils"
    }
)


# Purges
@nexaub_on_cmd(command=["purge"], modlue=mod_file, admins_only=True)
async def purge_this(_, message: Message):
  p_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  if not message.reply_to_message:
    return await p_msg.edit("`Reply to a message to starting purge from!`")
  await p_msg.delete()
  mid_list = []
  for mid in range(message.reply_to_message.message_id, message.message_id):
    mid_list.append(mid)
    # If there are more than 100 messages ub'll start deleting
    if len(mid_list) == 100:
      await NEXAUB.delete_messages(chat_id=message.chat.id, message_ids=mid_list, revoke=True) # Docs says revoke Defaults to True but...
      mid_list = []
    # Let's check if there are any other messages left to delete. Just like that 0.1% bacteria that can't be destroyed by soap
    if len(mid_list) > 0:
      await NEXAUB.delete_messages(chat_id=message.chat.id, message_ids=mid_list, revoke=True)


# Bans
@nexaub_on_cmd(command=["ban"], modlue=mod_file, admins_only=True)
async def ban_usr(_, message: Message):
  ban_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  is_me = await NEXAUB.get_me()
  args = int(get_arg(message))
  # Getting user id
  if args and args.isnumeric():
    b_user_id = str(args).replace("@", "")
  elif r_msg:
    if r_msg.from_user:
      b_user_id = r_msg.from_user.id
    else:
      return await ban_msg.edit("`Reply to a message from a user to ban!`")
  # User id checks
  if b_user_id in nexaub_devs:
    return await ban_msg.edit("`Lmao! Tryna ban my devs? Using me? 😂`")
  if b_user_id == is_me.id:
    return await ban_msg.edit("`Why should I ban my self?`")
  await message.chat.kick_member(user_id=int(b_user_id))
  await ban_msg.edit(f"**Banned 👊** \n\n**User ID:** `{b_user_id}`")


# Kick
@nexaub_on_cmd(command=["kick"], modlue=mod_file, admins_only=True)
async def kick_usr(_, message: Message):
  kick_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  is_me = await NEXAUB.get_me()
  args = get_arg(message)
  default_ban_time = 5
  # Getting user id
  if args:
    spl_args = args.split(None)
    if len(spl_args) == 2:
      b_user_id = str(spl_args[0]).replace("@", "")
      if spl_args[1].isdigit():
        default_ban_time = spl_args[1]
    elif len(spl_args) == 1:
      b_user_id = str(args).replace("@", "")
    else:
      return await kick_msg.edit("`Reply to a message from a user or give a user id to kick!`")
  elif r_msg:
    if r_msg.from_user:
      b_user_id = r_msg.from_user.id
    else:
      return await kick_msg.edit("`Reply to a message from a user to kick!`")
    if args and args.isdigit():
      default_ban_time = args
  # User id checks
  if b_user_id in nexaub_devs:
    return await kick_msg.edit("`Lmao! Tryna kick my devs? Using me? 😂`")
  if b_user_id == is_me.id:
    return await kick_msg.edit("`Why should I kick my self?`")  
  # Kicking the user
  await message.chat.kick_member(user_id=int(b_user_id))
  await kick_msg.edit(f"**Kicked ✊** \n\n**User ID:** `{b_user_id}` \n\n`⚠️ Unbanning after {default_ban_time} secs! ⚠️`")
  await asyncio.sleep(float(default_ban_time))
  await message.chat.unban_member(user_id=int(b_user_id))


# Unbans
@nexaub_on_cmd(command=["unban"], modlue=mod_file, admins_only=True)
async def unban_usr(_, message: Message):
  u_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  u_arg = get_arg(message)
  if r_msg:
    u_usr_id = r_msg.from_user.id
  elif u_arg:
    u_usr_id = u_arg
  else:
    return await u_msg.edit("`Give a user id to unban!`")
  await message.chat.unban_member(user_id=int(u_usr_id))
  await u_msg.edit(f"**Ubanned 🤝** \n\n**User ID:** `{u_usr_id}`")


# Pin message
@nexaub_on_cmd(command=["pin"], modlue=mod_file, admins_only=True, only_groups=True)
async def pin_msg(_, message: Message):
  pin_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  args = get_arg(message)
  if not r_msg:
    return await pin_msg.edit("`Reply to a message to pin it!`")
  if args and (args == "-dn"):
    await r_msg.pin(disable_notification=True)
  else:
    await r_msg.pin()
  await pin_msg.edit(f"[Message]({r_msg.link}) `Pinned successfully!`", disable_web_page_preview=True)


# Unpin message
@nexaub_on_cmd(command=["unpin"], modlue=mod_file, admins_only=True, only_groups=True)
async def unpin_msg(_, message: Message):
  unpin_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  args = get_arg(message)
  if args and (args == "-all"):
    chat_id = message.chat.id
    await NEXAUB.unpin_all_chat_messages(chat_id)
    await unpin_msg.edit("`Successfully unpinned all pinned messages in this chat!`")
  else:
    if not r_msg:
      return await unpin_msg.edit("`Reply to a pinned message to unpin it!`")
    await r_msg.unpin()
    await unpin_msg.edit(f"[Message]({r_msg.link}) `Unpinned successfully!`", disable_web_page_preview=True)