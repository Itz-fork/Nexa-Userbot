# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

from asyncio import sleep
from pyrogram.types import Message
from pyrogram.errors import FloodWait

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r, LOG_CHANNEL_ID
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.errors import Errors
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Spam,**

✘ `spam` - To spam a specific text
✘ `fspam` - To spam a specific photo / video

**Example:**

  ✘ `spam`,
   ⤷ Send with command = `{Config.CMD_PREFIX}spam Text to Spam`
   ⤷ Reply to a text message = `{Config.CMD_PREFIX}spam`
  
  **Tip 💡,**
    ⤷ You can limit the spam too. Just type limit after the command - `{Config.CMD_PREFIX}spam 5`

  ✘ `fspam`,
   ⤷ Same arguments and logic as spam command
""",
        f"{mod_name}_category": "unknown"
    }
)


# Function to spam the message while avoiding the floodwait
async def do_spam(limit, chat_id, spam_text=None, spam_message=None):
    # Sleep time (in seconds)
    sleep_time = 0.1 if limit <= 50 else 0.5 if limit <= 100 else 1
    spm_limit = int(limit)
    try:
        # Saves message in the log channel
        if spam_message:
            msg = await spam_message.copy(LOG_CHANNEL_ID)
        for i in range(0, spm_limit):
            if spam_text:
                await NEXAUB.send_message(chat_id, spam_text)
            elif msg:
                await msg.copy(chat_id)
            else:
                return
            await sleep(sleep_time)
        try:
            await msg.delete()
        except:
            pass
    except FloodWait as e:
        await sleep(e.x)
        return await do_spam(limit, chat_id, spam_text=None, spam_message=None)
    except BaseException as e:
        raise Errors.SpamFailed(e)


# Text spam
@nexaub.on_cmd(command=["spam"])
async def spam_text(_, message: Message):
    spm_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    args = get_arg(message)
    spam_limit = 10
    if r_msg:
        # Checks if the replied message has any text
        if not r_msg.text:
            return await spm_msg.edit(f"`Reply to a text message to spam it!` \n\nDid you meant `{Config.CMD_PREFIX}fspam` ?")
        to_spam = r_msg.text
        # Checks if spam limit is provided by the user
        if args and args.isnumeric():
            spam_limit = int(args)
    elif args:
        splt_args = args.split(None, 1)
        if len(splt_args) < 2:
            return await spm_msg.edit("`Give some text or reply to a text message to spam it!`")
        to_spam = splt_args[1]
        if splt_args[0].isnumeric():
            spam_limit = int(splt_args[0])
    else:
        return await spm_msg.edit("`Give some text or reply to a text message to spam it!`")
    await do_spam(spam_limit, message.chat.id, spam_text=to_spam)
    await spm_msg.edit(f"`Successfully spammed {spam_limit} messages!`")


# Doc / Audio / Video spam / Animation / Sticker (Basically copy of replied message)
@nexaub.on_cmd(command=["fspam"])
async def copy_spam(_, message: Message):
    spm_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    args = get_arg(message)
    spam_limit = 10
    if r_msg:
        # Checks if spam limit is provided by the user
        if args and args.isnumeric():
            spam_limit = int(args)
    else:
        return await spm_msg.edit("`Reply to a message to spam a copy of it!`")
    await do_spam(spam_limit, message.chat.id, spam_message=r_msg)
    await spm_msg.edit(f"`Successfully spammed {spam_limit} messages!`")