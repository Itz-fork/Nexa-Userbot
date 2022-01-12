# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from . import nexa_mongodb

nexaub_antif = nexa_mongodb["config_db"]


# To on / off / get anti functions
async def set_anti_func(var, value):
    anti_f = await nexaub_antif.find_one({"_id": var})
    if anti_f:
        await nexaub_antif.update_one({"_id": var}, {"$set": {"anti_funcs": value}})
    else:
        await nexaub_antif.insert_one({"_id": var, "anti_funcs": value})

async def get_anti_func(var):
    anti_f = await nexaub_antif.find_one({"_id": var})
    if not anti_f:
        return None
    else:
        g_custom_var = anti_f["anti_funcs"]
        return g_custom_var

async def del_anti_func(var):
    anti_f = await nexaub_antif.find_one({"_id": var})
    if anti_f:
        await nexaub_antif.delete_one({"_id": var})
        return True
    else:
        return False


# To set / remove anti functions chats
async def set_anti_func_chat(chat_id):
    antif_chat = await nexaub_antif.find_one({"_id": "ANTI_FUNCS_CHATS"})
    if antif_chat:
        await nexaub_antif.update_one({"_id": "ANTI_FUNCS_CHATS"}, {"$push": {"chat_ids": chat_id}})
    else:
        chat_iid = [chat_id]
        await nexaub_antif.insert_one({"_id": "ANTI_FUNCS_CHATS", "chat_ids": chat_iid})

async def get_anti_func_chat():
    antfui = await nexaub_antif.find_one({"_id": "ANTI_FUNCS_CHATS"})
    if antfui:
        return [int(antiC) for antiC in antfui.get("chat_ids")]
    else:
        return []

async def del_anti_func_chat(chat_id):
    r_sudo_id = await nexaub_antif.find_one({"_id": "ANTI_FUNCS_CHATS"})
    if r_sudo_id:
        await nexaub_antif.update_one({"_id": "ANTI_FUNCS_CHATS"}, {"$pull": {"chat_ids": chat_id}})
    else:
        return False