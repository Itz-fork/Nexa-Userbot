# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

from mega import Mega
from nexa_userbot.core.nexaub_database.nexaub_db_conf import get_custom_var

async def getMegaEmailandPass():
    m_email = await get_custom_var("MEGA_EMAIL")
    m_pass = await get_custom_var("MEGA_PASS")
    if not m_email or not m_pass:
        return None
    else:
        return [m_email, m_pass]

async def loginToMega(e_and_m):
    client = Mega().login(e_and_m[0], e_and_m[1])
    return client

def UploadToMega(msg, file, mega):
    try:
        uploadfile = mega.upload(f"{file}", upstatusmsg=msg)
        public_link = mega.get_upload_link(uploadfile)
        # Editing the message with uploaded link
        msg.edit(f"**Successfully Uploaded!** \n\n**Link:** {public_link}", disable_web_page_preview=True)
    except Exception as e:
        return msg.edit(f"**Error:** \n`{e}`")