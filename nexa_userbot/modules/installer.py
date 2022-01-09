# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

from pyrogram.types import Message
from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Plugin Installler,**

  ✘ `install` - To Install a Plugin

**Example:**

  ✘ `install`
   ⤷ Reply to pyrogram module made by Nexa UB Author with `{Config.CMD_PREFIX}install`


**Note:** `All Official Plugins are available at` **@NexaUBPlugins**! `Please don't install unofficial Plugins!`
""",
        f"{mod_name}_category": "userbot"
    }
)


@nexaub.on_cmd(command=["install"])
async def install_plugin(_, message: Message):
    msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    replied_msg = message.reply_to_message
    if not replied_msg:
        return await msg.edit("`Please reply to a valid python module to install!`")
    if not replied_msg.document:
        return await msg.edit("`Please reply to a valid python module to install!`")
    plugin_name = replied_msg.document.file_name
    plugin_path = f"nexa_userbot/modules/Extras/{plugin_name}"
    plugin_extension = plugin_name.split(".")[1].lower()
    plugin_name_no_exe = plugin_name.split(".")[0]
    if plugin_extension != "py":
        return await msg.edit("`This file isn't a python file`")
    if os.path.isfile(plugin_path):
        return await msg.edit("`Plugin already installed!`")
    await replied_msg.download(file_name=plugin_path)
    try:
        await msg.edit("`Loading Plugin, Please wait...`")
        nexaub().import_plugin(plugin_path)
        await msg.edit(f"**Successfully Loaded Plugin** \n\n** ✗ Plugin Name:** `{plugin_name_no_exe}`")
    except Exception as e:
        await msg.edit(f"**Error:** {e}")