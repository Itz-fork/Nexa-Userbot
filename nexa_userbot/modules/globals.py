# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os

from pyrogram import filters
from pyrogram.types import Message

from . import nexaub_devs
from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r, nexaub_on_cf, SUDO_IDS
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.nexaub_database.nexaub_db_gbans import gban_usr, get_gbanned, get_gban_reason, ungban_usr
from nexa_userbot.helpers.pyrogram_help import get_ma_chats


# Help
CMD_HELP.update(
    {
        "globals": """
**Globals,**

  ✘ `gban` - To Gban a user (Reply to a user or send this command with user id)
  ✘ `ungban` - To UnGban a user
  ✘ `gbans` - To Get Gbanned User List

**Example:**

  ✘ `gban`,
   ⤷ by Userid = `.gban 1234567 Test Gban`
   ⤷ by Username = `.gban @Spammer_Guy Test Gban`
   ⤷ Or Just Reply to a message from user with reason to Gban!

  ✘ `gban`,
   ⤷ by Userid = `.ungban 1234567`
   ⤷ by Username = `.ungban @Spammer_Guy`
   ⤷ Or Just Reply to a message from user to UnGban!
"""
    }
)

mod_file = os.path.basename(__file__)

@nexaub_on_cmd(command="gban", modlue=mod_file)
async def me_goin_oflin(_, message: Message):
    gban_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    gban_rsn = get_arg(message)
    nexaub_owner = await NEXAUB.get_me()
    if r_msg:
        if gban_rsn:
            gban_rson = gban_rsn
        else:
            gban_rson = "That guy is a creepy scammer!"
        gban_uid = r_msg.from_user.id
    elif gban_rsn:
        gets_user_arg = gban_rsn.split(None)
        gban_rson = gets_user_arg[1]
        gban_uid = gets_user_arg[0]
        if gban_uid.isnumeric():
            gban_uid = gban_uid
        else:
            if "@" in gban_uid:
                usr_name = gban_uid.replace("@", "").split(None)[0]
            else:
                usr_name = gban_uid
            get_usr_info = await NEXAUB.get_users(usr_name)
            gban_uid = get_usr_info.id
    else:
        return await gban_msg.edit("`Give a User ID, Username or Reply to a user message to Gban`")
    if gban_uid in nexaub_devs:
        return await gban_msg.edit("`Sorry I can't Gban Dev of me")
    if gban_uid == nexaub_owner.id:
        return await gban_msg.edit("`Wtf? You are trying to gban yourself?`")
    is_gbanned = await get_gban_reason(gban_uid)
    if is_gbanned:
        return await gban_msg.edit("`Lmao, That shit guy is already GBANNED!`")
    await gban_msg.edit("`Fetching Chats For Gban Process...`")
    f_chats = await get_ma_chats()
    if not f_chats:
        return await gban_msg.edit("`No Chats to Gban! Lmao!`")
    total_f_chats = len(f_chats)
    for gokid in f_chats:
        ub_failed = 0
        try:
            await NEXAUB.kick_chat_member(chat_id=gokid, user_id=int(gban_uid))
        except:
            ub_failed += 1
    await gban_usr(gban_id=gban_uid, gban_reason=gban_rson)
    await gban_msg.edit(f"**#USER_GBANNED** \n\n**User:** `{gban_uid}` \n**Reason:** `{gban_rson}` \n**Total Chats:** `{total_f_chats-ub_failed}`")


@nexaub_on_cmd(command="ungban", modlue=mod_file)
async def me_goin_oflin(_, message: Message):
    ungban_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_ug_msg = message.reply_to_message
    gban_usr = get_arg(message)
    if gban_usr:
        if gban_usr.isnumeric():
            ungban_uid = gban_usr
        else:
            if "@" in gban_usr:
                usr_name = gban_usr.replace("@", "").split(None)[0]
            else:
                usr_name = gban_usr
            get_him = await NEXAUB.get_users(usr_name)
            ungban_uid = get_him.id
    else:
        ungban_uid = r_ug_msg.from_user.id
    await ungban_msg.edit("`Fetching Your Chats...`")
    ung_chats = await get_ma_chats()
    if not ung_chats:
        return await ungban_msg.edit("`No Chats to Gban! Lmao!`")
    total_ung_chats = len(ung_chats)
    is_gbanned = await get_gban_reason(ungban_uid)
    if is_gbanned is None:
        return await ungban_msg.edit("`Is this user Gbanned?`")
    for good_boi in ung_chats:
        ub_failed = 0
        try:
            await NEXAUB.unban_chat_member(chat_id=good_boi, user_id=ungban_uid)
        except:
            ub_failed += 1
    await ungban_usr(ungban_uid)
    await ungban_msg.edit(f"**#UN_GBANNED** \n\n**User:** `{ungban_uid}` \n**Affected To:** `{total_ung_chats-ub_failed} Chats`")


@nexaub_on_cmd(command="gbans", modlue=mod_file)
async def me_goin_oflin(_, message: Message):
    glist_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    gban_list = await get_gbanned()
    total_gbans = len(gban_list)
    gban_txt = "**#GBAN_LIST** \n\n"
    if total_gbans == 0:
        return await glist_msg.edit("`There isn't any Gbanned User!`")
    for gb in gban_list:
        gban_txt += f" ⤷ **User:** `{gb['gbanned_usr']}` \n ⤷ **Reason:** `{gb['reason_for_gban']}`"
    if len(gban_txt) > 4096:
        file = open("NEXAUB_Gban_List.txt", "w+")
        file.write(gban_txt)
        file.close()
        await NEXAUB.send_document(
            message.chat.id,
            "NEXAUB_Gban_List.txt",
            caption=f"Gban List"
        )
        os.remove("NEXAUB_Gban_List.txt")
    else:
        await glist_msg.edit(gban_txt)


@nexaub_on_cf(filters.incoming & ~filters.me & ~filters.user(SUDO_IDS))
async def gbanner(_m, message: Message):
    if not message:
        return
    if not message.from_user:
        return
    gbanned_usr_id = message.from_user.id
    if not gbanned_usr_id:
        return
    is_gbanned = await get_gban_reason(gbanned_usr_id)
    gban_chat_id = message.chat.id
    if is_gbanned:
        if message.chat.type == "private":
            await NEXAUB.block_user(gbanned_usr_id)
        else:
            try:
                await NEXAUB.kick_chat_member(chat_id=gban_chat_id, user_id=gbanned_usr_id)
            except:
                return
        await NEXAUB.send_message(chat_id=gban_chat_id, text=f"**#GBAN_DB** \n`Gbanned User Joined to this chat. So I've Banned Him!` \n\n**User ID:** `{gbanned_usr_id}` \n**Reason:** `{is_gbanned}`")
    else:
        return