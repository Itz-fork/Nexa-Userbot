# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from . import nexa_mongodb

nexaub_sudos = nexa_mongodb["sudos_db"]

# ========== Databse for sudo users ==========

# Add sudo user to database
async def add_sudo(sudo_id):
    isudo_id = int(sudo_id)
    sudo_db = await nexaub_sudos.find_one({"_id": "SUDO_USERS"})
    if sudo_db:
        await nexaub_sudos.update_one({"_id": "SUDO_USERS"}, {"$push": {"sudo_id": isudo_id}})
    else:
        isudo_id = [isudo_id]
        await nexaub_sudos.insert_one({"_id": "SUDO_USERS", "sudo_id": isudo_id})

# Get sudo users from database
async def get_sudos():
    s_u_i = await nexaub_sudos.find_one({"_id": "SUDO_USERS"})
    if s_u_i:
        return [int(sudo_id) for sudo_id in s_u_i.get("sudo_id")]
    else:
        return []

# Remove sudo user from databse
async def remove_sudo(sudo_id):
    r_sudo_id = await nexaub_sudos.find_one({"_id": "SUDO_USERS"})
    irudo_id = int(sudo_id)
    if r_sudo_id:
        await nexaub_sudos.update_one({"_id": "SUDO_USERS"}, {"$pull": {"sudo_id": irudo_id}})
    else:
        return False

# Check if user already in sudo databse
async def check_if_sudo(sudo_id):
    already_sudo = await nexaub_sudos.find_one({"_id": "SUDO_USERS"})
    if already_sudo:
        sudo_list = [int(sudo_id) for sudo_id in already_sudo.get("sudo_id")]
        if int(sudo_id) in sudo_list:
            return True
        else:
            return False
    else:
        return False