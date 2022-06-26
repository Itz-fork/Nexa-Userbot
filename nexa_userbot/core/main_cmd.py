# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os
import logging
import asyncio
import importlib

from pyrogram import filters, enums
from pyrogram.handlers import MessageHandler
from pyrogram.errors.exceptions.bad_request_400 import MessageIdInvalid

from nexa_userbot.core.nexaub_database.nexaub_db_conf import get_log_channel
from nexa_userbot.core.nexaub_database.nexaub_db_sudos import get_sudos
from nexa_userbot.helpers.pyrogram_help import rm_markdown
from nexa_userbot import NEXAUB
from config import Config


# ================= MAIN ================= #
# Log channel id
log_cid_loop = asyncio.get_event_loop()
LOG_CHANNEL_ID = log_cid_loop.run_until_complete(get_log_channel())

# Sudo users
sudos = log_cid_loop.run_until_complete(get_sudos())
sudos.append("me")
SUDO_IDS = sudos



# Edit or reply
async def e_or_r(nexaub_message, msg_text, parse_mode="md", disable_web_page_preview=True):
    """
    Arguments:

        ``nexaub_message``: Message object
        ``msg_text``: Text that you want to perform the task
        ``parse_mode`` (optional): Parse mode (Defaults to markdown)
        ``disable_web_page_preview`` (optional): Pass False if you don't want to disable web page preview (Defaults to True)
    """
    message = nexaub_message
    if not message:
        return await message.edit(msg_text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
    if not message.from_user:
        return await message.edit(msg_text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
    if message.from_user.id in SUDO_IDS:
        if message.reply_to_message:
            return await message.reply_to_message.reply_text(msg_text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
        else:
            return await message.reply_text(msg_text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)
    else:
        return await message.edit(msg_text, parse_mode=parse_mode, disable_web_page_preview=disable_web_page_preview)


class nexaub:
    """
    ## Main class of Nexa Userbot

    ## Available Functions:
    
        ``on_cmd``: Main decorator
        ``on_cf``: Decorator to handle custom filters
        ``add_handler``: Add handler to userbot
    """
    @classmethod
    def on_cmd(
        self,
        command: list,
        group: int = 0,
        admins_only: bool = False,
        only_pm: bool = False,
        only_groups: bool = False,
        no_sudos: bool = False
    ):
        """
        ## Main decorator

        ### Arguments:

            ``command``: List of commands
            ``group`` (optional): Handler group (Defaults to 0)
            ``admins_only`` (optional): True if the command is only for admins (Defaults to False)
            ``only_pm`` (optional): True if the command is only for private chats (Defaults to False)
            ``only_groups`` (optional): True if the command is only for groups / supergroups (Defaults to False)
            ``no_sudos`` (optional): True if the command is restricted for sudo users (Defaults to False)
        """
        if no_sudos:
            nexaub_filter = (filters.me & filters.command(command, Config.CMD_PREFIX) & ~filters.via_bot & ~filters.forwarded)
        else:
            nexaub_filter = (filters.user(SUDO_IDS) & filters.command(command, Config.CMD_PREFIX) & ~filters.via_bot & ~filters.forwarded)
        def decorate_nexaub(func):
            async def x_wrapper(client, message):
                nexaub_chat_type = message.chat.type
                if admins_only:
                    if nexaub_chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL]:
                        usr = await NEXAUB.get_me()
                        how_usr = await message.chat.get_member(usr.id)
                        if how_usr.status in ["creator", "administrator"]:
                            pass
                        else:
                            return await e_or_r(nexaub_message=message, msg_text="`First you need to be an admin of this chat!`")
                    # It's PM Bois! Everyone is an admin in PM!
                    else:
                        pass
                if only_pm and nexaub_chat_type != enums.ChatType.PRIVATE:
                    return await e_or_r(nexaub_message=message, msg_text="`Yo, this command is only for PM!`")
                if only_groups and nexaub_chat_type not in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
                    return await e_or_r(nexaub_message=message, msg_text="`Is this even a group?`")
                try:
                    await func(client, message)
                except MessageIdInvalid:
                    logging.warning("Don't delete message while processing. It may crash the bot!")
                except BaseException as e:
                    logging.error(f"\nModule - {func.__module__} | Command: {command[0]} | Traceback: \n{e}")
                    error_text = f"""
**#ERROR**

**Module:** `{func.__module__}`
**Command:** `{Config.CMD_PREFIX + command[0]}`
**Traceback:**
`{e}`

**Forward this to @NexaUB_Support**
"""
                    if len(error_text) > 4000:
                        clean_error_text = await rm_markdown(error_text)
                        file = open("error_nexaub.txt", "w+")
                        file.write(clean_error_text)
                        file.close()
                        await NEXAUB.send_document(LOG_CHANNEL_ID, "error_nexaub.txt", caption="`Error of Nexa Userbot`")
                        os.remove("error_nexaub.txt")
                    else:
                        await NEXAUB.send_message(chat_id=LOG_CHANNEL_ID, text=error_text)
            self.add_handler(x_wrapper, nexaub_filter, group)
            return x_wrapper
        return decorate_nexaub
    
    # Custom filter handling (Credits: Friday Userbot)
    @classmethod
    def on_cf(self, custom_filters, handler_group: int = 0):
        """
        ## Decorator to handle custom filters

        ### Arguments:

            ``custom_filters``: Custom filters to handle
            ``handler_group`` (optional): Handler group (Defaults to 0)
        """
        def decorate_nexaub_cf(func):
            async def x_wrapper_cf(client, message):
                try:
                    await func(client, message)
                except MessageIdInvalid:
                    logging.warning("Don't delete message while processing. It may crash the bot!")
                except BaseException as e:
                    logging.error(f"\nModule - {func.__module__} | Command: (Noting, Custom Filter)")
                    error_text = f"""
**#ERROR**

**Module:** `{func.__module__}`
**Command:** `(Noting, Custom Filter)`
**Traceback:**
`{e}`

**Forward this to @NexaUB_Support**
"""
                    if len(error_text) > 4000:
                        clean_error_text = await rm_markdown(error_text)
                        file = open("error_nexaub.txt", "w+")
                        file.write(clean_error_text)
                        file.close()
                        await NEXAUB.send_document(LOG_CHANNEL_ID, "error_nexaub.txt", caption="`Error of Nexa Userbot`")
                        os.remove("error_nexaub.txt")
                    else:
                        await NEXAUB.send_message(chat_id=LOG_CHANNEL_ID, text=error_text)
                message.continue_propagation()
            self.add_handler(x_wrapper_cf, custom_filters, handler_group)
            return x_wrapper_cf
        return decorate_nexaub_cf
    
    @classmethod
    def add_handler(self, x_wrapper, nexaub_filter, cmd_grp):
        """
        ## Add handler to the userbot

        ### Arguments:

            ``x_wrapper``: Callback function
            ``nexaub_filter``: Filters
            ``cmd_grp``: Command Group
        """
        NEXAUB.add_handler(MessageHandler(x_wrapper, filters=nexaub_filter), group=cmd_grp)
    
    # Thanks for Friday Userbot for the idea
    def import_plugin(self, p_path):
        """
        ## Loads custom plugins

        ### Arguments:

            ``p_path``: Path to the plugin
        """
        nexaub_xplugin = p_path.replace("/", ".")
        try:
            importlib.import_module(nexaub_xplugin)
            logging.info(f" LOADED PLUGIN: - {os.path.basename(p_path)}")
        except:
            logging.warn(f" FAILED TO LOAD PLUGIN: - {os.path.basename(p_path)}")
    
    async def resolve_peer(self, pr, max_tries=1, counted=0):
        """
        ## Returns the InputPeer of a known peer id

        ### Arguments:
        
            ``pr``: Peer id
            ``max_tries`` (optional): Maximum number of times that userbot needs to try (Defaults to 1)
            ``counted`` (optional): Defaults to 0 (Don't pass any)
        """
        tri_c = counted
        try:
            return await NEXAUB.resolve_peer(pr)
        except:
            tri_c += 1
            if not tri_c >= max_tries:
                return await self.resolve_peer(pr, counted=tri_c)