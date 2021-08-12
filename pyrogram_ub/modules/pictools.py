# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Friday Userbot | DevsExpo

from pyrogram import filters
from pyrogram.methods.chats import restrict_chat_member
from pyrogram.types import Message

from pyrogram_ub import NEXAUB, CMD_HELP
from pyrogram_ub.helpers.pictool_help import gib_carbon_sar
from config import Config

CMD_HELP.update(
    {
        "pictools": """
**Picure Tools**


  ✘ `carbon` - To Carbonize a text
"""
    }
)

# Carbon a text
@NEXAUB.on_message(filters.command("carbon", Config.CMD_PREFIX) & filters.me)
async def gibcarbon(_, message: Message):
    r_msg = message.reply_to_message
    carbon_msg = await message.edit_text("`Processing...`")
    if not r_msg:
        await carbon_msg.edit("`Reply to a Text Message Lol!`")
        return
    if not r_msg.text:
        await carbon_msg.edit("`Reply to a Text Message Lol!`")
        return
    carboned_pic = await gib_carbon_sar(r_msg.text)
    await carbon_msg.edit("`Uploading...`")
    await NEXAUB.send_photo(message.chat.id, carboned_pic)
    await carbon_msg.delete()
    carboned_pic.close()
