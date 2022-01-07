# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os

from pyrogram import filters
from pyrogram.types import Message
from datetime import datetime

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.nexaub_database.nexaub_db_afk import me_afk, get_afk, me_online
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Afk,**

  ✘ `afk` - To Activate Afk Module

**Example:**

  ✘ `afk`,
   ⤷ Send with reason = `{Config.CMD_PREFIX}afk This is the reason`
   
  **Tip 💡,**
   ⤷ Send with `-del` flag to delete sent afk messages when you come back online = `{Config.CMD_PREFIX}afk -del This is the reason`
""",
        f"{mod_name}_category": "utils"
    }
)


# Dict to store messaged users details temporarily
AFK_SPAMMER_DB = {}
# List to store all afk messages that sent to chats
AFK_MSGS_DB = {}


# Check if afk
async def u_afk_bro(filter, client, message):
    if_afk = await get_afk()
    if if_afk:
        return True
    else:
        return False

# Creating a custom filter
ya_afk = filters.create(func=u_afk_bro, name="is_ya_afk")


@nexaub.on_cmd(command=["afk"])
async def me_goin_oflin(_, message: Message):
    afk_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    get_afk_reason = get_arg(message)
    if get_afk_reason:
        splitted_txt = get_afk_reason.split(None, 1)
        if splitted_txt[0] == "-del":
            del_afk_msgs_af = True
            if len(splitted_txt) >= 2:
                afk_reason = splitted_txt[1]
            else:
                afk_reason = "I'm Busy For Now! Will Come Online Later :)"
        else:
            del_afk_msgs_af = False
            afk_reason = get_afk_reason
    else:
        afk_reason = "I'm Busy For Now! Will Come Online Later :)"
        del_afk_msgs_af = False
    afk_time = datetime.now().replace(microsecond=0)
    await me_afk(afk_time=afk_time, afk_reason=afk_reason, delete_afk_msgs=del_afk_msgs_af)
    await afk_msg.edit(f"**I'm Going AFK** \n\n**Reason:** `{afk_reason}`")


@nexaub.on_cf(
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
    # Checking if user spammed before, if yes ub won't reply to that user again
    usr_id = message.from_user.id
    if usr_id in AFK_SPAMMER_DB:
        AFK_SPAMMER_DB[usr_id] += 1
        if AFK_SPAMMER_DB[usr_id] >= 6:
            return
    else:
        AFK_SPAMMER_DB[usr_id] = 1
    # If user messaged you 5 times bot'll send him a nice reply :)
    if AFK_SPAMMER_DB[usr_id] == 5:
        return await message.reply("`Enough! You've messaged my master 5 times, Go get some brain you dumb ass!`")
    s_time, a_reason, should_del_afks = await get_afk()
    now_time = datetime.now().replace(microsecond=0)
    afk_time = str((now_time - s_time))
    afk_reply = await message.reply(f"**I'm AFK** \n\n**Last Online:** `{afk_time}` \n**Reason:** `{a_reason}`")
    # Saving current chat id and replied message id to a dict to delete when the user come back online
    if should_del_afks:
        afk_chat_id = message.chat.id
        if afk_chat_id in AFK_MSGS_DB:
            msg_list = AFK_MSGS_DB[afk_chat_id]
            msg_list.append(afk_reply.message_id)
            AFK_MSGS_DB[afk_chat_id] = msg_list
        else:
            AFK_MSGS_DB[afk_chat_id] = [afk_reply.message_id]

@nexaub.on_cf(
    filters.me
    & filters.outgoing
    & ya_afk
)
async def back_online_bois(_, message: Message):
    s_time, a_reason, should_del_afks = await get_afk()
    com_online = datetime.now().replace(microsecond=0)
    afk_time = str((com_online - s_time))
    await me_online()
    await message.reply(f"**I'm No Longer AFK** \n\n**Afk Time:** `{afk_time}` \n**Reason:** `{a_reason}`")
    # Deleting send afk messages
    if should_del_afks:
        status_msg = await message.reply("`Deleting sent afk messages...`")
        for c_id, msgs_ids in AFK_MSGS_DB.items():
            await NEXAUB.delete_messages(chat_id=c_id, message_ids=msgs_ids)
        await status_msg.delete()
