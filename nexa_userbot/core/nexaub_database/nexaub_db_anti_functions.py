# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from . import nexa_mongodb

nexaub_antif = nexa_mongodb["anti_functionsdb"]


# To on / off / get anti functions
async def set_anti_func(chat_id, status, mode):
    anti_f = await nexaub_antif.find_one({"_id": chat_id})
    if anti_f:
        await nexaub_antif.update_one({"_id": chat_id}, {"$set": {"status": status, "mode": mode}})
    else:
        await nexaub_antif.insert_one({"_id": chat_id, "status": status, "mode": mode})

async def get_anti_func(chat_id):
    anti_f = await nexaub_antif.find_one({"_id": chat_id})
    if not anti_f:
        return None
    else:
        snm = [anti_f["status"], anti_f["mode"]]
        return snm

async def del_anti_func(chat_id):
    anti_f = await nexaub_antif.find_one({"_id": chat_id})
    if anti_f:
        await nexaub_antif.delete_one({"_id": chat_id})
        return True
    else:
        return False