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
BAN_EVENT_TXT = """
**Ban Event❗**

**User:** {}
**Due to:** `Containing {} letters in the name / message`"
"""

async def anti_func_handler(_, __, msg):
    chats = await get_anti_func(msg.chat.id)
    if chats:
        return True
    else:
        False

anti_chats = filters.create(func=anti_func_handler)

# I know there is lots of code duplication but oh well, IDGF
@nexaub.on_cf(anti_chats & (filters.new_chat_members | filters.text))
async def check_anti_funcs(_, message: Message):
    # Users list
    users = message.new_chat_members
    chat_id = message.chat.id
    # Obtaining message text and user
    text = message.text
    tuser = message.from_user
    anti_func_det = await get_anti_func(chat_id)
    # Checks if the functions are enabled for the chat
    if not anti_func_det:
        return
    if anti_func_det[0] != "on":
        return
    # Checks for anti arabic
    if anti_func_det[1] == "ar":
        try:
            if users:
                for user in users:
                    if any(search(REGEXES.arab, name) for name in [user.first_name, user.last_name]):
                        await NEXAUB.ban_chat_member(chat_id, user.id)
                        await message.reply(BAN_EVENT_TXT.format(user.mention, "arabic"))
            elif text:
                if not tuser:
                    return
                if search(REGEXES.arab, text):
                    await NEXAUB.ban_chat_member(chat_id, tuser.id)
                    await message.reply(BAN_EVENT_TXT.format(tuser.mention, "arabic"))
        except:
            pass
    # Checks for anti chinese
    elif anti_func_det[1] == "zh":
        try:
            if users:
                for user in users:
                    if any(search(REGEXES.chinese, name) for name in [user.first_name, user.last_name]):
                        await NEXAUB.ban_chat_member(chat_id, user.id)
                        await message.reply(BAN_EVENT_TXT.format(user.mention, "chinese"))
            elif text:
                if not tuser:
                    return
                if search(REGEXES.chinese, text):
                    await NEXAUB.ban_chat_member(chat_id, tuser.id)
                    await message.reply(BAN_EVENT_TXT.format(tuser.mention, "chinese"))
        except:
            pass
    # Checks for anti japanese
    elif anti_func_det[1] == "jp":
        try:
            if users:
                for user in users:
                    if any(search(REGEXES.japanese, name) for name in [user.first_name, user.last_name]):
                        await NEXAUB.ban_chat_member(chat_id, user.id)
                        await message.reply(BAN_EVENT_TXT.format(user.mention, "japanese"))
            elif text:
                if not tuser:
                    return
                if search(REGEXES.japanese, text):
                    await NEXAUB.ban_chat_member(chat_id, tuser.id)
                    await message.reply(BAN_EVENT_TXT.format(tuser.mention, "japanese"))
        except:
            pass
    # Checks for anti russian
    elif anti_func_det[1] == "rs":
        try:
            if users:
                for user in users:
                    if any(search(REGEXES.cyrillic, name) for name in [user.first_name, user.last_name]):
                        await NEXAUB.ban_chat_member(chat_id, user.id)
                        await message.reply(BAN_EVENT_TXT.format(user.mention, "russian"))
            elif text:
                if not tuser:
                    return
                if search(REGEXES.cyrillic, text):
                    await NEXAUB.ban_chat_member(chat_id, tuser.id)
                    await message.reply(BAN_EVENT_TXT.format(tuser.mention, "russian"))
        except:
            pass