# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from . import nexa_mongodb

nexaub_pm_guard = nexa_mongodb["pm_gurad_db"]


# Add a user to approved users database
async def add_approved_user(user_id):
    good_usr = int(user_id)
    does_they_exists = await nexaub_pm_guard.find_one({"_id": "APPROVED_USERS"})
    if does_they_exists:
        await nexaub_pm_guard.update_one({"_id": "APPROVED_USERS"}, {"$push": {"good_id": good_usr}})
    else:
        await nexaub_pm_guard.insert_one({"_id": "APPROVED_USERS", "good_id": [good_usr]})


# Remove a user from approved users database
async def rm_approved_user(user_id):
    bad_usr = int(user_id)
    does_good_ones_exists = await nexaub_pm_guard.find_one({"_id": "APPROVED_USERS"})
    if does_good_ones_exists:
        await nexaub_pm_guard.update_one({"_id": "APPROVED_USERS"}, {"$pull": {"good_id": bad_usr}})
    else:
        return None

# Check if a user in approved users database
async def check_user_approved(user_id):
    random_usr = int(user_id)
    does_good_users_exists = await nexaub_pm_guard.find_one({"_id": "APPROVED_USERS"})
    if does_good_users_exists:
        good_users_list = [cool_user for cool_user in does_good_users_exists.get("good_id")]
        if random_usr in good_users_list:
            return True
        else:
            return False
    else:
        return False