# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os
import asyncio

from pyrogram import idle
from nexa_userbot import NEXAUB
from nexa_userbot.modules import *
from nexa_userbot.helpers.pyrogram_help import import_plugin
from nexa_userbot.core.nexaub_database.nexaub_db_conf import get_custom_var
from nexa_userbot.core.startup_checks import check_or_set_log_channel, check_arq_api


# Plugin installer for channels
async def download_custom_plugins():
    g_plugin_channels = await get_custom_var("CUSTOM_PLUGINS_CHANNELS")
    if g_plugin_channels:
        plugin_channels = list(g_plugin_channels)
        print("Downloading Custom Plugins...")
        try:
            for channel in plugin_channels:
                async for plugin in NEXAUB.search_messages(chat_id=channel, query=".py", filter="document"):
                    plugin_name = plugin.document.file_name
                    if not os.path.exists(f"nexa_userbot/modules/Extras/{plugin_name}"):
                        await NEXAUB.download_media(message=plugin, file_name=f"nexa_userbot/modules/{plugin_name}")
        except Exception as e:
            return print(f"Error \n\n{e} \n\nUnable to install plugins from custom plugin channels!")
    else:
        return print("No Custom Plugin Channels were specified, Nexa-Userbot is running with default plugins only!")


# Custom plugin collector
async def install_custom_plugins():
    custom_plugin_path = "nexa_userbot/modules/Extras"
    if os.path.isdir(custom_plugin_path):
        try:
            for plugin in os.listdir(custom_plugin_path):
                if plugin.endswith(".py"):
                    import_plugin(os.path.join(custom_plugin_path, plugin))
        except:
            pass



async def main_startup():
    print("""
|| Nexa Userbot ||

Copyright (c) 2021 Itz-fork
"""
    )
    await NEXAUB.start()
    # Check or set log channel id
    log_channel_id = await check_or_set_log_channel()
    # Downloading and installing Custom Plugins
    print(".......................")
    await download_custom_plugins()
    await install_custom_plugins()
    print(".......................")
    # Check if arq api is available else it'll obtain a one
    await check_arq_api()
    try:
        await NEXAUB.send_message(chat_id=log_channel_id[1], text="`Nexa Userbot is alive!`")
    except:
        print("WARNING: There was an error while creating the LOG CHANNEL please add a one manually!")
    await idle()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main_startup())