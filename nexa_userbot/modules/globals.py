# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os

from pyrogram import filters
from pyrogram.types import Message

from . import nexaub_devs
from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r, SUDO_IDS
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.nexaub_database.nexaub_db_globals import gban_usr, get_gbanned, get_gban_reason, ungban_usr
from nexa_userbot.helpers.pyrogram_help import get_ma_chats
from config import Config

# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Globals,**

  ✘ `gban` - To Gban a user (Reply to a user or send this command with user id)
  ✘ `ungban` - To UnGban a user
  ✘ `gbans` - To Get Gbanned User List
  ✘ `gpromote` - To Promote a user globally
  ✘ `gdemote` - To Demote a user globally

**Example:**

  ✘ `gban`,
   ⤷ by Userid = `{Config.CMD_PREFIX}gban 1234567 Test Gban`
   ⤷ by Username = `{Config.CMD_PREFIX}gban @Spammer_Guy Test Gban`
   ⤷ Or Just Reply to a message from user with reason to Gban!

  ✘ `gban`,
   ⤷ by Userid = `{Config.CMD_PREFIX}ungban 1234567`
   ⤷ by Username = `{Config.CMD_PREFIX}ungban @Spammer_Guy`
   ⤷ Or Just Reply to a message from user to UnGban!

  ✘ `gpromote`,
   ⤷ by Userid / Username = `{Config.CMD_PREFIX}gpromote 1234567`
   ⤷ Or Just Reply to a message from user to Gpromote!
   
   **Tips 💡,**
    ⤷ Define which chat types the user needed to be promoted - `{Config.CMD_PREFIX}gpromote [group/channel/all]`
    ⤷ Define the user's permission role - `{Config.CMD_PREFIX}gpromote [basic/god]`

  ✘ `gdemote`,
   ⤷ Same arguments and logic as gpromote
""",
        f"{mod_name}_category": "utils"
    }
)


# Gban
@nexaub.on_cmd(command=["gban"])
async def gbun_dis_usr(_, message: Message):
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
        return await gban_msg.edit("`No Chats to Gban!`")
    total_f_chats = len(f_chats)
    for gokid in f_chats:
        ub_failed = 0
        try:
            await NEXAUB.ban_chat_member(chat_id=gokid, user_id=int(gban_uid))
        except:
            ub_failed += 1
    await gban_usr(gban_id=gban_uid, gban_reason=gban_rson)
    await gban_msg.edit(f"**#USER_GBANNED** \n\n**User:** `{gban_uid}` \n**Reason:** `{gban_rson}` \n**Total Chats:** `{total_f_chats-ub_failed}`")


# Ungban
@nexaub.on_cmd(command=["ungban"])
async def ungbun_dis_usr(_, message: Message):
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
        if r_ug_msg:
            ungban_uid = r_ug_msg.from_user.id
        else:
            return await ungban_msg.edit("`Reply to a message from a user or give a user id to UnGban that user!`")
    await ungban_msg.edit("`Fetching Your Chats...`")
    ung_chats = await get_ma_chats()
    if not ung_chats:
        return await ungban_msg.edit("`No Chats to Gban!`")
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
    await ungban_msg.edit(f"**#USER_UNGBANNED** \n\n**User:** `{ungban_uid}` \n**Affected To:** `{total_ung_chats-ub_failed}` **Chats**")


# Gbans
@nexaub.on_cmd(command=["gbans"])
async def gbuns_in_whole_time(_, message: Message):
    glist_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    gban_list = await get_gbanned()
    total_gbans = len(gban_list)
    gban_txt = "**#GBAN_LIST** \n\n"
    if total_gbans == 0:
        return await glist_msg.edit("`There aren't any Gbanned User!`")
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


# Gpromote
@nexaub.on_cmd(command=["gpromote"])
async def gpromote_dis_usr(_, message: Message):
    gpromote_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    options_args = get_arg(message)
    nexaub_owner = await NEXAUB.get_me()
    # Getting user id and options
    if r_msg:
        # Parsing arguments
        if options_args:
            base_options = options_args.split(" ")
            if len(base_options) == 2:
                where = base_options[0]
                role = base_options[1]
            elif len(base_options) == 1:
                where = base_options[0]
                role = None
        else:
            return await gpromote_msg.edit("`Give user id or username to promote that user globally!")
        if message.from_user:
            uid = r_msg.from_user.id
        else:
            return await gpromote_msg.edit("`Reply to a message from a user!`")
    elif options_args:
        # Parsing arguments
        base_option_args = options_args.split(" ")
        if len(base_option_args) == 3:
            uid = base_option_args[0]
            where = base_option_args[1]
            role = base_option_args[2]
        elif len(base_option_args) == 2:
            uid = base_option_args[0]
            where = base_option_args[1]
            role = None
        elif len(base_option_args) == 1:
            uid = base_option_args[0]
            where = None
            role = None
        else:
            return await gpromote_msg.edit("`Give user id or username to promote that user globally!`")
    else:
        return await gpromote_msg.edit("`Give a User ID, Username or Reply to a user message to Gpromote!`")
    
    # Checking user id
    if not uid.isnumeric():
        if "@" in uid:
            usrname = uid.replace("@", "")
            gp_user_id = (await NEXAUB.get_users(usrname)).id
        else:
            return await gpromote_msg.edit("`Give a user id or username to promote that user globally!`")
    else:
        gp_user_id = int(uid)
    # Checking gpromote places
    if where in ["group", "channel", "all"]:
        if where == "all":
            where_to_promote = ["group", "supergroup", "channel"]
        elif where == "group":
            where_to_promote = ["group", "supergroup"]
        else:
            where_to_promote = ["channel"]
    else:
        return await gpromote_msg.edit("`Invalid chat type!` \n\n**Use:**\n ⤷ `all` - All chat types (private, group and channel) \n ⤷ `group` - Groups only \n ⤷ `channel` - Channels only")
    # Checking role
    if not role:
        gp_role = "basic"
    elif role.lower() in ["basic", "god"]:
        gp_role = role.lower()
    else:
        return await gpromote_msg.edit("`Invalid gpromote role!` \n\n**Use:**\n ⤷ `basic` - User will able to manage chats/voice chats, post/pin messages and invite users. \n ⤷ `god` - Users will get all the permissions a admin can get.")
    if gp_user_id == nexaub_owner.id:
        return await gpromote_msg.edit("`Wtf? You are trying to gpromote yourself?`")
    # Fetching chats
    await gpromote_msg.edit("`Fetching Chats For Gpromote...`")
    gp_chats = await get_ma_chats(chat_types=where_to_promote)
    if not gp_chats:
        return await gpromote_msg.edit("`No Chats to Gpromote!`")
    total_gp_chats = len(gp_chats)
    # Promoting the user
    for gp_u_chat in gp_chats:
        ub_failed = 0
        try:
            if gp_role == "basic":
                await NEXAUB.promote_chat_member(
                    chat_id=gp_u_chat,
                    user_id=gp_user_id,
                    can_manage_chat=True,
                    can_manage_voice_chats=True,
                    can_post_messages=True,
                    can_pin_messages=True,
                    can_invite_users=True
                )
            else:
                await NEXAUB.promote_chat_member(
                    chat_id=gp_u_chat,
                    user_id=gp_user_id,
                    can_manage_chat=True,
                    can_change_info=True,
                    can_post_messages=True,
                    can_edit_messages=True,
                    can_delete_messages=True,
                    can_restrict_members=True,
                    can_invite_users=True,
                    can_pin_messages=True,
                    can_promote_members=True,
                    can_manage_voice_chats=True
                )
        except:
            ub_failed += 1
    await gpromote_msg.edit(f"**#USER_GPROMOTED** \n\n**Globally promoted** {(await NEXAUB.get_users(gp_user_id)).mention} **in ** `{total_gp_chats - ub_failed}` **chats!**")


# Gdemote
@nexaub.on_cmd(command=["gdemote"])
async def gdemote_dis_usr(_, message: Message):
    gdemote_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    uid_args = get_arg(message)
    nexaub_owner = await NEXAUB.get_me()
    if r_msg:
        if message.from_user:
            uid = r_msg.from_user.id
        else:
            return await gdemote_msg.edit("`Reply to a message from a user!`")
        if uid_args:
            where = uid_args
    elif uid_args:
        base_args = uid_args.split(" ")
        if len(base_args) == 2:
            uid = base_args[0]
            where = base_args[1]
        elif len(base_args) == 1:
            uid = base_args[0]
        else:
            return await gdemote_msg.edit("`Give a User ID, Username or Reply to a user message to Gdemote!`")
    else:
        return await gdemote_msg.edit("`Give a User ID, Username or Reply to a user message to Gdemote!`")
    # Checking user id
    if not uid.isnumeric():
        if "@" in uid:
            usrname = uid.replace("@", "")
            gd_user_id = (await NEXAUB.get_users(usrname)).id
        else:
            return await gdemote_msg.edit("`Give a user id or username to demote that user globally!`")
    else:
        gd_user_id = int(uid)
    if gd_user_id == nexaub_owner.id:
        return await gdemote_msg.edit("`Wtf? You are trying to gdemote yourself?`")
    # Checking gdemote places
    if where in ["group", "channel", "all"]:
        if where == "all":
            where_to_promote = ["group", "supergroup", "channel"]
        elif where == "group":
            where_to_promote = ["group", "supergroup"]
        else:
            where_to_promote = ["channel"]
    else:
        return await gdemote_msg.edit("`Invalid chat type!` \n\n**Use:**\n ⤷ `all` - All chat types (private, group and channel) \n ⤷ `group` - Groups only \n ⤷ `channel` - Channels only")
    # Fetching chats
    await gdemote_msg.edit("`Fetching Chats For Gdemote...`")
    gp_chats = await get_ma_chats(chat_types=where_to_promote)
    if not gp_chats:
        return await gdemote_msg.edit("`No Chats to Gdemote!`")
    total_gp_chats = len(gp_chats)
    # Promoting the user
    for gd_u_chat in gp_chats:
        ub_failed = 0
        try:
            await NEXAUB.promote_chat_member(
                chat_id=gd_u_chat,
                user_id=gd_user_id,
                can_manage_chat=False,
                can_change_info=False,
                can_post_messages=False,
                can_edit_messages=False,
                can_delete_messages=False,
                can_restrict_members=False,
                can_invite_users=False,
                can_pin_messages=False,
                can_promote_members=False,
                can_manage_voice_chats=False
            )
        except:
            ub_failed += 1
    await gdemote_msg.edit(f"**#USER_GDEMOTED** \n\n**Globally demoted** {(await NEXAUB.get_users(gd_user_id)).mention} **in ** `{total_gp_chats - ub_failed}` **chats!**")


@nexaub.on_cf(filters.incoming & ~filters.me & ~filters.user(SUDO_IDS))
async def gbanner(_, message: Message):
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
                await NEXAUB.ban_chat_member(chat_id=gban_chat_id, user_id=gbanned_usr_id)
                await NEXAUB.send_message(chat_id=gban_chat_id, text=f"**#GBAN_DB** \n`Gbanned User Joined to this chat. So I've Banned Him!` \n\n**User ID:** `{gbanned_usr_id}` \n**Reason:** `{is_gbanned}`")
            except:
                return await NEXAUB.send_message(chat_id=gban_chat_id, text=f"**#GBAN_DB** \n`Gbanned User Joined to this chat!` \n\n**User ID:** `{gbanned_usr_id}` \n**Reason:** `{is_gbanned}`")
    else:
        return
