# Copyright (c) 2021 Itz-fork
# Part of: Nexa Userbot
# Experimantal Mega.nz Downloader Plugin (Uses megatools)

import os
import subprocess
import shutil

from pyrogram.types import Message
from functools import partial
from asyncio import get_running_loop
from fsplit.filesplit import Filesplit

from nexa_userbot import CMD_HELP
from nexa_userbot.helpers.up_to_tg import guess_and_send
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Mega Downloader,**

  ✘ `megadl` - To Download Files / Folder from Mega.nz

**Example:**

  ✘ `megadl`
   ⤷ Send with command = `{Config.CMD_PREFIX}megadl https://mega.nz/file/#43445234` (Link is fake tho)

**Both files and folders are supported**
""",
        f"{mod_name}_category": "tools"
    }
)


# Run bash cmd in python
def nexa_mega_runner(command):
    run = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    shell_ouput = run.stdout.read()[:-1].decode("utf-8")
    return shell_ouput

# Splitting large files
def split_files(input_file, out_base_path):
    nexa_fs = Filesplit()
    split_file = input_file
    split_fsize = 2040108421
    out_path = out_base_path
    nexa_fs.split(file=split_file, split_size=split_fsize, output_dir=out_path)

@nexaub.on_cmd(command=["megadl"])
async def megatoolsdl(_, message: Message):
    megatools_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    url = message.text
    cli_user_id = str(message.from_user.id)
    cli_download_path = f"{os.getcwd()}/NexaUb/Megatools/{str(message.from_user.id)}"
    if len(message.command) < 2:
        return await megatools_msg.edit("`Please send a valid mega.nz link to download!`")
    # Mega url to download
    cli_url = url.split(None, 1)[1]
    # Checking if sent message has a vaild mega.nz url
    if "https://mega.nz/" not in url:
        return await megatools_msg.edit("`Please send a valid mega.nz link to download!`")
    # Checking if there is a ongoing task for the user
    if os.path.isdir(cli_download_path):
        return await megatools_msg.edit("`Already One Process is Going On. Please wait until it's finished!`")
    else:
        os.makedirs(cli_download_path)
    await megatools_msg.edit(f"`Starting to download file / folder from mega.nz!` \n\nThis may take sometime. Depends on your file / folder size.")
    megacmd = f"megadl --limit-speed 0 --path {cli_download_path} {cli_url}"
    loop = get_running_loop()
    await loop.run_in_executor(None, partial(nexa_mega_runner, megacmd))
    nexaub_path_f = f"{os.getcwd()}/NexaUb/Megatools/{str(message.from_user.id)}"
    folder_f = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(nexaub_path_f)] for val in sublist]
    await megatools_msg.edit("`Downloading Finished! Trying to upload now`")
    try:
        for nexa_m in folder_f:
            file_size = os.stat(nexa_m).st_size
            if file_size > 2040108421:
                split_out_dir = nexaub_path_f + "splitted_files"
                await megatools_msg.edit("`Large File Detected, Trying to split it!`")
                loop = get_running_loop()
                await loop.run_in_executor(None, partial(split_files(input_file=nexa_m, out_base_path=split_out_dir)))
                await megatools_msg.edit("`Splitting Finished! Uploading Now...`")
                for splitted_f in split_out_dir:
                    await guess_and_send(input_file=splitted_f, chat_id=message.chat.id, thumb_path="cache")
            else:
                await guess_and_send(input_file=nexa_m, chat_id=message.chat.id, thumb_path="cache")
        await megatools_msg.edit("`Uploading Finished!`")
    except Exception as e:
        await megatools_msg.edit(f"**Error:** `{e}`")
    try:
        shutil.rmtree(nexaub_path_f)
    except Exception as e:
        await megatools_msg.edit(f"**Error:** `{e}`")