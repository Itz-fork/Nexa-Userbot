# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

from pyrogram import filters
from pyrogram.types import Message
from re import search

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.nexaub_database.nexaub_db_anti_functions import set_anti_func , get_anti_func, del_anti_func
from nexa_userbot.helpers.regexes import REGEXES
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Anti-Functions,**

✘ `antiarab` - To enable anti-arab function
✘ `antichinese` - To enable anti-chinese function
✘ `antijapanese` - To enable anti-japanese function
✘ `antirussian` - To enable anti-russian function

**Example:**

  ✘ For all commands,
   ⤷ To on = `{Config.CMD_PREFIX}COMMAND_HERE on`
   ⤷ To off = `{Config.CMD_PREFIX}COMMAND_HERE off`


  **Ex:**
   ⤷ To on = `{Config.CMD_PREFIX}antiarab on`
   ⤷ To off = `{Config.CMD_PREFIX}antiarab off`
""",
        f"{mod_name}_category": "tools"
    }
)


# Enable anti-arab
@nexaub.on_cmd(command=["antiarab"], admins_only=True, only_groups=True)
async def on_off_antiarab(_, message: Message):
    antiarab_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    args = get_arg(message)
    if not args:
        return await antiarab_msg.edit(f"**Invalid Usage!** \n\n **⤷ To on = `{Config.CMD_PREFIX}antiarab on` \n ⤷ To off = `{Config.CMD_PREFIX}antiarab off`")
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "ar")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await antiarab_msg.edit(f"**Invalid Usage!** \n\n **⤷ To on = `{Config.CMD_PREFIX}antiarab on` \n ⤷ To off = `{Config.CMD_PREFIX}antiarab off`")
    await antiarab_msg.edit(f"**Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Anti Arabic module!**")

# Enable anti-chinesee
@nexaub.on_cmd(command=["antichinese"], admins_only=True, only_groups=True)
async def on_off_antichinese(_, message: Message):
    antichinese_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    args = get_arg(message)
    if not args:
        return await antichinese_msg.edit(f"**Invalid Usage!** \n\n **⤷ To on = `{Config.CMD_PREFIX}antichinese on` \n ⤷ To off = `{Config.CMD_PREFIX}antichinese off`")
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "zh")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await antichinese_msg.edit(f"**Invalid Usage!** \n\n **⤷ To on = `{Config.CMD_PREFIX}antichinese on` \n ⤷ To off = `{Config.CMD_PREFIX}antichinese off`")
    await antichinese_msg.edit(f"**Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Anti Chinese module!**")

# Enable anti-japanese
@nexaub.on_cmd(command=["antijapanese"], admins_only=True, only_groups=True)
async def on_off_antijapanese(_, message: Message):
    antijapanese_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    args = get_arg(message)
    if not args:
        return await antijapanese_msg.edit(f"**Invalid Usage!** \n\n **⤷ To on = `{Config.CMD_PREFIX}antijapanese on` \n ⤷ To off = `{Config.CMD_PREFIX}antijapanese off`")
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "jp")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await antijapanese_msg.edit(f"**Invalid Usage!** \n\n **⤷ To on = `{Config.CMD_PREFIX}antijapanese on` \n ⤷ To off = `{Config.CMD_PREFIX}antijapanese off`")
    await antijapanese_msg.edit(f"**Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Anti Japanese module!**")

# Enable anti-russian
@nexaub.on_cmd(command=["antirussian"], admins_only=True, only_groups=True)
async def on_off_antirussian(_, message: Message):
    antirussian_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    args = get_arg(message)
    if not args:
        return await antirussian_msg.edit(f"**Invalid Usage!** \n\n **⤷ To on = `{Config.CMD_PREFIX}antirussian on` \n ⤷ To off = `{Config.CMD_PREFIX}antirussian off`")
    lower_args = args.lower()
    if lower_args == "on":
        await set_anti_func(message.chat.id, "on", "rs")
    elif lower_args == "off":
        await del_anti_func(message.chat.id)
    else:
        return await antirussian_msg.edit(f"**Invalid Usage!** \n\n **⤷ To on = `{Config.CMD_PREFIX}antirussian on` \n ⤷ To off = `{Config.CMD_PREFIX}antirussian off`")
    await antirussian_msg.edit(f"**Successfully** `{'Enabled' if lower_args=='on' else 'Disabled'}` **Anti Russian module!**")


# Listen to new members and checks
ANTIF_WARNS_DB = {}
ANTIF_TO_DEL = {}

WARN_EVEN_TXT = """
**Warn Event❕**

**User:** {}
**Due to:** `Containing {} letters in the name / message`

`Be careful ⚠️: You have {}/3 warns, after that you'll be banned forever!`
"""
BAN_EVENT_TXT = """
**Ban Event❗**

**User:** {}
**Due to:** `Containing {} letters in the name / message and warns exceeded!`
"""

FORM_AND_REGEXES = {
    "ar": [REGEXES.arab, "arabic"],
    "zh": [REGEXES.chinese, "chinese"],
    "jp": [REGEXES.japanese, "japanese"],
    "rs": [REGEXES.cyrillic, "russian"]
}

async def anti_func_handler(_, __, msg):
    chats = await get_anti_func(msg.chat.id)
    if chats:
        return True
    else:
        False

# Function to check if the user is an admin
async def check_admin(msg, user_id):
    if msg.chat.type in ["group", "supergroup", "channel"]:
        how_usr = await msg.chat.get_member(user_id)
        if how_usr.status in ["creator", "administrator"]:
            return True
        else:
            return False
    else:
        return True

# Function to save user's warns in a dict
async def check_afdb(user_id):
    if user_id in ANTIF_WARNS_DB:
        ANTIF_WARNS_DB[user_id] += 1
        if ANTIF_WARNS_DB[user_id] >= 3:
            return True
        return False
    else:
        ANTIF_WARNS_DB[user_id] = 1
        return False

# Function to warn or ban users
async def warn_or_ban(message, mode):
    # Users list
    users = message.new_chat_members
    chat_id = message.chat.id
    # Obtaining user who sent the message
    tuser = message.from_user
    try:
        mdnrgx = FORM_AND_REGEXES[mode]
        if users:
            for user in users:
                if any(search(mdnrgx[0], name) for name in [user.first_name, user.last_name]):
                    await NEXAUB.ban_chat_member(chat_id, user.id)
                    await message.reply(BAN_EVENT_TXT.format(user.mention, mdnrgx[1]))
        elif message.text:
            if not tuser:
                return
            if search(mdnrgx[0], message.text):
                # Admins have the foking power
                if not await check_admin(message, tuser.id):
                    # Ban the user if the warns are exceeded
                    if await check_afdb(tuser.id):
                        await NEXAUB.ban_chat_member(chat_id, tuser.id)
                        await message.reply(BAN_EVENT_TXT.format(tuser.mention, mdnrgx[1]))
                    await message.delete()
                    rp = await message.reply(WARN_EVEN_TXT.format(tuser.mention, mdnrgx[1], ANTIF_WARNS_DB[tuser.id]))
                    if chat_id in ANTIF_TO_DEL:
                        await NEXAUB.delete_messages(chat_id=chat_id, message_ids=ANTIF_TO_DEL[chat_id])
                    ANTIF_TO_DEL[chat_id] = [rp.message_id]
    except:
        pass

anti_chats = filters.create(func=anti_func_handler)


@nexaub.on_cf(anti_chats & (filters.new_chat_members | filters.text))
async def check_anti_funcs(_, message: Message):
    anti_func_det = await get_anti_func(message.chat.id)
    # Checks if the functions are enabled for the chat
    if not anti_func_det:
        return
    if anti_func_det[0] != "on":
        return
    # Warns or ban the user from the chat
    await warn_or_ban(message, anti_func_det[1])