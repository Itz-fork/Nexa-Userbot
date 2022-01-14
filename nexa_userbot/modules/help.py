# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot
import os
import re

from pyrogram.types import Message

from . import __all__ as ALL_MODULES
from .Extras import get_xtra_modules_names
from nexa_userbot import CMD_HELP
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from config import Config


mod_file = os.path.basename(__file__)


# Removing last comma from variables
async def rm_last_comma(text):
    index = text.rfind(",")
    if not index < 0:
        return text[:index] + "" + text[index+1:]
    else:
        return text

# Configs
DEFAULT_HELP_TXT = """
**Available Modules**

{userbot_help}

{dev_help}

{tools_help}

{utils_help}

{unknown_help}


`{cmd_prfx}help [module name]`
"""

CUSTOM_HELP_TXT = """
**Available Custom Modules**

{userbot_help}

{dev_help}

{tools_help}

{utils_help}

{unknown_help}


`{cmd_prfx}xhelp [module name]`
"""

async def get_help_type(htx):
    if re.search(r'\bxhelp|chelp\b', htx):
        help_list = [sorted(await get_xtra_modules_names()), CUSTOM_HELP_TXT]
    else:
        help_list = [sorted(ALL_MODULES), DEFAULT_HELP_TXT]
    return help_list

@nexaub.on_cmd(command=["help", "xhelp", "chelp"])
async def help(_, message: Message):
    args = get_arg(message)
    help_user_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    MODULE_LIST = await get_help_type(message.text.split(" ")[0])
    if not args:
        # Base texts
        base_userbot_txt = "**🧭 Userbot:** "
        base_dev_txt = "**👨‍💻 Dev:** "
        base_tools_txt = "**⚙️ Tools:** "
        base_utils_txt = "**🗂 Utils:** "
        base_unknown_txt = "**🥷 Unknown:** "
        # Generating help menu text
        for module in MODULE_LIST[0]:
            # Checks the category of the module
            cat = CMD_HELP.get(f"{module}_category", False)
            if cat == "userbot":
                base_userbot_txt += f"`{module}`, "
            elif cat == "dev":
                base_dev_txt += f"`{module}`, "
            elif cat == "tools":
                base_tools_txt += f"`{module}`, "
            elif cat == "utils":
                base_utils_txt += f"`{module}`, "
            else:
                base_unknown_txt += f"`{module}`, "
        # Removing last comma from the text
        userbot_txt = await rm_last_comma(base_userbot_txt)
        dev_txt = await rm_last_comma(base_dev_txt)
        tools_txt = await rm_last_comma(base_tools_txt)
        utils_txt = await rm_last_comma(base_utils_txt)
        unknown_txt = await rm_last_comma(base_unknown_txt)
        await help_user_msg.edit(MODULE_LIST[1].format(
            userbot_help=userbot_txt,
            dev_help=dev_txt,
            tools_help=tools_txt,
            utils_help=utils_txt,
            unknown_help=unknown_txt,
            cmd_prfx=Config.CMD_PREFIX
        ))
    else:
        module_help = CMD_HELP.get(args, False)
        if not module_help:
            return await help_user_msg.edit("`Invalid Module Name!`")
        else:
            await help_user_msg.edit(module_help)