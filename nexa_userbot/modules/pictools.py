# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os
import requests

from pyrogram.types import Message
from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.helpers.pictool_help import gib_carbon_sar
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from nexa_userbot.core.nexaub_database.nexaub_db_conf import get_custom_var
from config import Config


# Help
CMD_HELP.update(
    {
        "pictools": f"""
**Picure Tools**

  ✘ `carbon` - To Carbonize a text
  ✘ `rmbg` - To Remove Background from Image using remove.bg API

**Example:**

  ✘ `carbon`,
   ⤷ Send command with text to make a carbon = `{Config.CMD_PREFIX}carbon Carbon Text`
   ⤷ Reply to a text message to carbon it = `{Config.CMD_PREFIX}carbon` (Reply to a text message)

  ✘ `rmbg`,
   ⤷ Reply to a text message with `{Config.CMD_PREFIX}rmbg`
"""
    }
)

mod_file = os.path.basename(__file__)

# Carbon a text
# Credits: Friday Userbot | DevsExpo
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


# Function to get remove.bg api key
async def get_rmbg_api():
    try:
        rmbg_bg_api = await get_custom_var("RMBG_API_KEY")
        return rmbg_bg_api
    except:
        return None

# Background Remover
@nexaub_on_cmd(command="rmbg", modlue=mod_file)
async def removebg(_, message: Message):
    rmbg_api = await get_rmbg_api()
    rmbg_r_msg = message.reply_to_message
    rmbg_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    if rmbg_api is None:
        return await rmbg_msg.edit(f"**Remove BG API is not in Database ❗️** \nSet it using `{Config.CMD_PREFIX}setvar RMBG_API_KEY your_api_key` \n\n__**Don't Know How to get your API Key? [Read This](https://nexa-userbot.netlify.app/docs/get-started/configs/#get-rmbg_api_key)**__", disable_web_page_preview=True)
    if not rmbg_r_msg:
        return await rmbg_msg.edit("`Give a Photo to Remove Background from It!`")
    if not rmbg_r_msg.photo:
        return await rmbg_msg.edit("`Give a Photo to Remove Background from It!`")
    else:
        rmbg_image = await rmbg_r_msg.download()
        rmbg_header = requests.post(
    'https://api.remove.bg/v1.0/removebg',
    files={'image_file': open(rmbg_image, 'rb')},
    data={'size': 'auto'},
    headers={'X-Api-Key': rmbg_api},
    )
    if rmbg_header.status_code == requests.codes.ok:
        with open("NEXAUB-rmbg.png", "wb") as rmbg_out_image:
            rmbg_out_image.write(rmbg_header.content)
            await NEXAUB.send_photo(chat_id=message.chat.id, photo="NEXAUB-rmbg.png")
            os.remove("NEXAUB-rmbg.png")
    else:
        return await rmbg_msg.edit(f"**Error:** \nError Code `{rmbg_header.status_code}` and Error is `{rmbg_header.text}`")
