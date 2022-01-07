# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os
import asyncio

from pyrogram.types import Message
from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Hack**

✘ `hack` - To perform a hack prank
""",
        f"{mod_name}_category": "unknown"
    }
)


@nexaub.on_cmd(command=["hack", "heck"])
async def heck_dat(_, message: Message):
    r_msg = message.reply_to_message
    heck_msg = await e_or_r(nexaub_message=message, msg_text="**[root@Nexa-Ub]** `enable tg-hacker && clear`")
    if not r_msg:
        return await heck_msg.edit("`⚠ Reply to a telegram user to perform a hack!`")
    if not r_msg.from_user:
        return await heck_msg.edit("`⚠ Reply to a telegram user to perform a hack!`")
    # User info
    user_id = r_msg.from_user.id
    user_mention = r_msg.from_user.mention
    user_dc = r_msg.from_user.dc_id
    # Hack animation characters (stage 1)
    stage1_msg = ""
    hack_animation_stage1_chars = [
        "**[root@Nexa-Ub]** `tg-hacker init` \n",
        "`>> Initializing telegram hacker...` \n\n",
        "**[root@Nexa-Ub]** `tg-hacker --check-tools` \n",
        "`>> Checking if the required tools are installed...` \n",
        "`>> Done Checking! All the tools are installed!` \n\n",
        f"**[root@Nexa-Ub]** `mkdir {user_id}` \n",
        f"`>> Creating Directory for the user...` \n",
        "`>> Successfully Created the Directory!` \n\n",
        f"**[root@Nexa-Ub]** `cd {user_id} && tg-hacker --set-config-user-path pwd && cd` \n",
        f"\n`Forwarding the process to stage 2`"
    ]
    # Hack animation characters (stage 2)
    stage2_msg = ""
    hack_animation_stage2_chars = [
        "**[root@Nexa-Ub]** `tg-hacker --connect-to-server --most-stable` \n",
        "`>> Connecting to the telegram servers...` \n"
        "`>> Connected ✓` \n\n",
        "**[root@Nexa-Ub]** `tg-hacker --collect-user-info --less-verbose` \n"
        f"`>> Extracting the information about user id - {user_id}` \n",
        f"`>> Process completed ✓. Collected information about` {user_mention} . \n"
        "\n`Forwarding the process to stage 3`"
    ]
    # Hack animation characters (stage 3)
    stage3_msg = ""
    hack_animation_stage3_progress = [
        "`▱▱▱▱▱▱▱▱▱▱▱▱▱ 0%` \n",
        "`▰▱▱▱▱▱▱▱▱▱▱▱▱ 5%` \n",
        "`▰▱▱▱▱▱▱▱▱▱▱▱▱ 14%` \n",
        "`▰▰▱▱▱▱▱▱▱▱▱▱▱ 23%`\n",
        "`▰▰▰▰▱▱▱▱▱▱▱▱▱ 31%` \n",
        "`▰▰▰▰▰▱▱▱▱▱▱▱▱ 43%` \n",
        "`▰▰▰▰▰▰▰▱▱▱▱▱▱ 59%` \n",
        "`▰▰▰▰▰▰▰▰▱▱▱▱▱ 65%` \n",
        "`▰▰▰▰▰▰▰▰▰▰▱▱▱ 78%` \n",
        "`▰▰▰▰▰▰▰▰▰▰▰▱▱ 89%` \n",
        "`▰▰▰▰▰▰▰▰▰▰▰▰▱ 94%` \n",
        "`▰▰▰▰▰▰▰▰▰▰▰▰▰ 100%` \n"
    ]
    hack_animation_stage3_chars = [
        "**[root@Nexa-Ub]** `tg-hacker start --use-tg-brut --less-verbose --auto-cmd` \n",
        "`>> Starting the hack...` \n",
        "`>> Downloading Telegram-Bruteforce-8.3.2.tar.gz (1.9MiB)` \n"
        "`>> Download Completed ✓` \n\n",
        "**[root@Nexa-Ub]** `tg-hacker --check-config` \n",
        "`>> Checking user config file...` \n"
        f"`>> Found config file - {user_id}.conf` \n",
        "**[root@Nexa-Ub]** `tg-hacker --upload` \n",
        f"`>> Uploading the hacked accound details to telegram server - ID {user_dc if user_dc else 'Main'}` \n\n",
    ]
    # Hack animation characters (stage 4)
    stage4_msg = ""
    hack_animation_stage4_chars = [
        "**[root@Nexa-Ub]** `tg-hacker check-if-completed` \n",
        "`>> Checking...` \n"
        "`>> Hacking completed ✓` \n\n",
        "**[root@Nexa-Ub]** `tg-hacker show --fix-for-tg-msg` \n\n\n",
        f"**Dear {user_mention}, Your telegram account has been hacked by me ☠! \nYou have to pay at least $98 to fix your telegram account!**"
    ]
    # Editing the message (stage 1)
    for char1 in hack_animation_stage1_chars:
        await asyncio.sleep(1)
        stage1_msg += char1
        await heck_msg.edit(stage1_msg)
    await asyncio.sleep(3)
    # Editing the message (stage 2)
    await heck_msg.edit(f"{stage1_msg} \n\n**[root@Nexa-Ub]** `clear`")
    for char2 in hack_animation_stage2_chars:
        await asyncio.sleep(2)
        stage2_msg += char2
        await heck_msg.edit(stage2_msg)
    await asyncio.sleep(4)
    # Editing the message (stage 3)
    await heck_msg.edit(f"{stage2_msg} \n\n**[root@Nexa-Ub]** `clear && tg-hacker --set-stage stage3`")
    for char3 in hack_animation_stage3_chars:
        await asyncio.sleep(3)
        stage3_msg += char3
        await heck_msg.edit(stage3_msg)
    await asyncio.sleep(3)
    for prgs in hack_animation_stage3_progress:
        await asyncio.sleep(3) 
        actual_prgs_msg = stage3_msg + prgs
        await heck_msg.edit(actual_prgs_msg)
    await asyncio.sleep(4)
    # Editing the message (stage 4)
    await heck_msg.edit(f"{actual_prgs_msg} \n**[root@Nexa-Ub]** `clear && tg-hacker --set-stage stage4`")
    for char4 in hack_animation_stage4_chars:
        await asyncio.sleep(3)
        stage4_msg += char4
        await heck_msg.edit(stage4_msg)