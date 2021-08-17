# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot

from pyrogram import filters
from pyrogram.types import Message
from pyrogram_ub import NEXAUB, HELP, CMD_HELP
from config import Config
from pyrogram_ub.helpers.pyrogram_help import get_arg

HELP.update(
    {
        "**🧭 Userbot**": "`alive`, `installer`, `updater`",
        "**👨‍💻 Dev**": "`eval`",
        "**⚙️ Tools**": "`paste`, `short_url`, `search`, `pictools`, `extractor`, `megatools`",
        "**🗂 Utils**": "`stickers`, `owner`",
        "\n**Usage**": "`.help [module_name]`"
    }
)


@NEXAUB.on_message(filters.command("help", Config.CMD_PREFIX) & filters.me)
async def help(_, message: Message):
    args = get_arg(message)
    help_user_msg = await message.edit("`Processing...`")
    if not args:
        text = "**Available Commands**\n\n"
        for key, value in HELP.items():
            text += f"{key}: {value}\n\n"
        await help_user_msg.edit(text)
        return
    else:
        module_help = CMD_HELP.get(args, False)
        if not module_help:
            await help_user_msg.edit("`Invalid Module Name!`")
            return
        else:
            await help_user_msg.edit(module_help)
