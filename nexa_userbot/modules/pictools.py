# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Friday Userbot | DevsExpo
import os
from pyrogram.types import Message

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.helpers.pictool_help import gib_carbon_sar
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from config import Config


# Help
CMD_HELP.update(
    {
        "pictools": """
**Picure Tools**


  ✘ `carbon` - To Carbonize a text
"""
    }
)

mod_file = os.path.basename(__file__)

# Carbon a text
@nexaub_on_cmd(command="carbon", modlue=mod_file)
async def gibcarbon(_, message: Message):
    r_msg = message.reply_to_message
    carbon_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    carbonpic_msg = get_arg(message)
    if not carbonpic_msg:
        if not r_msg:
            await carbon_msg.edit("`Reply to a Text Message Lol!`")
            return
        if not r_msg.text:
            await carbon_msg.edit("`Reply to a Text Message Lol!`")
            return
        else:
            carbonpic_msg = r_msg.text
    carboned_pic = await gib_carbon_sar(carbonpic_msg)
    await carbon_msg.edit("`Uploading...`")
    await NEXAUB.send_photo(message.chat.id, carboned_pic)
    await carbon_msg.delete()
    carboned_pic.close()