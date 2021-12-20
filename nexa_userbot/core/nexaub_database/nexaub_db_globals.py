# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from . import nexa_mongodb

nexaub_gban = nexa_mongodb["gban_db"]
# I'm lazy to implement both into one, so Do NOT question!
nexaub_other_globals = nexa_mongodb["other_globals"]


## Gban
# Database for storing gban details
async def gban_usr(gban_id, gban_reason="Abusing People!"):
    gban_user_id = int(gban_id)
    p_gbanned = await nexaub_gban.find_one({"gbanned_usr": gban_user_id})
    if p_gbanned:
        return True
    else:
        await nexaub_gban.insert_one({"gbanned_usr": gban_user_id, "reason_for_gban": gban_reason})

# Get gbanned user list
# Credits: Friday Userbot
async def get_gbanned():
    return [gban_usrs async for gban_usrs in nexaub_gban.find({})]

# Get gbaned reason
async def get_gban_reason(gban_id):
    gban_user_id = int(gban_id)
    pr_gbanned = await nexaub_gban.find_one({"gbanned_usr": gban_user_id})
    if pr_gbanned:
        return pr_gbanned["reason_for_gban"]
    else:
        return None

# Ungban a user
async def ungban_usr(gban_id):
    gban_user_id = int(gban_id)
    alr_gbanned = await nexaub_gban.find_one({"gbanned_usr": gban_user_id})
    if alr_gbanned:
        await nexaub_gban.delete_one({"gbanned_usr": gban_user_id})
    else:
        return False


## Gpromote
DEFAULT_CONFIGURATION = {
    "is_anonymous": False,
    "can_manage_chat": True,
    "can_change_info": True,
    "can_post_messages": True,
    "can_delete_messages": True,
    "can_restrict_members": True,
    "can_invite_users": True,
    "can_pin_messages": True,
    "can_promote_members": True,
    "can_manage_voice_chats": True
}