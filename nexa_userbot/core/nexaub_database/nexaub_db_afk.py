# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from . import nexa_mongodb

nexaub_afk = nexa_mongodb["afk_db"]

# Database for afk module
async def me_afk(afk_time, afk_reason="Busy 😴"):
    p_afk = await nexaub_afk.find_one({"_id": "ME_AFK"})
    if p_afk:
        await nexaub_afk.update_one({"_id": "ME_AFK"}, {"$set": {"g_afk_time": afk_time, "g_afk_reason": afk_reason}})
    else:
        await nexaub_afk.insert_one({"_id": "ME_AFK", "g_afk_time": afk_time, "g_afk_reason": afk_reason})

async def get_afk():
    alr_afk = await nexaub_afk.find_one({"_id": "ME_AFK"})
    if alr_afk:
        afk_time = alr_afk["g_afk_time"]
        afk_reason = alr_afk["g_afk_reason"]
        return afk_time, afk_reason
    else:
        return None

async def me_online():
    r_afk = await nexaub_afk.find_one({"_id": "ME_AFK"})
    if r_afk:
        await nexaub_afk.delete_one({"_id": "ME_AFK"})
    else:
        return False