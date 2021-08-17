# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os
import importlib
import logging

from pyrogram import filters
from pyrogram.types import Message
from nexa_userbot import NEXAUB, CMD_HELP
from config import Config

CMD_HELP.update(
    {
        "installer": """
**Plugin Installler,**

  ✘ `install` - To Install a Plugin

**Note:** `All Official Plugins are available at` **@NexaUBPlugins**! `Please don't install unofficial Plugins!`
"""
    }
)

# Load Plugins | Thanks for Friday Userbot for the idea
def import_plugin(p_name):
    nexa_plugin_path = "nexa_userbot.modules." + p_name
    importlib.import_module(nexa_plugin_path)
    logging.info(f"LOADED PLUGIN: - {p_name} - Nexa-Userbot")


@NEXAUB.on_message(filters.me & filters.command("install", Config.CMD_PREFIX))
async def install_plugin(_, message: Message):
    msg = await message.edit("`Processing...`")
    replied_msg = message.reply_to_message
    if not replied_msg:
        await msg.edit("`Please reply to a valid python module to install!`")
        return
    if not replied_msg.document:
        await msg.edit("`Please reply to a valid python module to install!`")
        return
    plugin_name = replied_msg.document.file_name
    plugin_path = f"nexa_userbot/modules/{plugin_name}"
    plugin_extension = plugin_name.split(".")[1].lower()
    plugin_name_no_exe = plugin_name.split(".")[0]
    if plugin_extension != "py":
        await msg.edit("`This file isn't a python file`")
        return
    if os.path.isfile(plugin_path):
        await msg.edit("`Plugin already installed!`")
        return
    await replied_msg.download(file_name=plugin_path)
    try:
        await msg.edit("`Loading Plugin, Please wait...`")
        import_plugin(plugin_name_no_exe)
        await msg.edit(f"**Successfully Loaded Plugin** \n\n** ✗ Plugin Name:** `{plugin_name_no_exe}`")
    except Exception as e:
        await msg.edit(f"**Error:** {e}")
