# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os
import shutil

from pyrogram import filters
from pyrogram.types import Message
from py_extract import Video_tools

from pyrogram_ub import NEXAUB, CMD_HELP
from config import Config

CMD_HELP.update(
    {
        "extractor": """
**Extractor**

  ✘ `ext_aud` - To Extract all audios from a video
"""
    }
)


@NEXAUB.on_message(filters.command("ext_aud", Config.CMD_PREFIX) & filters.me)
async def extract_all_aud(_, message: Message):
    replied_msg = message.reply_to_message
    ext_text = await message.edit("`Processing...`")
    ext_out_path = "./NexaUb/py_extract/audios"
    if not replied_msg:
        await ext_text.edit("`Please reply to a valid video file!`")
        return
    if not replied_msg.video:
        await ext_text.edit("`Please reply to a valid video file!`")
        return
    if os.path.exists(ext_out_path):
        await ext_text.edit("`Already one process is going on. Please wait till it finish!`")
        return
    replied_video = replied_msg.video
    try:
        await ext_text.edit("`Downloading...`")
        ext_video = await NEXAUB.download_media(message=replied_video)
        await ext_text.edit("`Extracting Audio(s)...`")
        exted_aud = Video_tools.extract_all_audio(input_file=ext_video)
        await ext_text.edit("`Extracting Finished! Now Uploading to Telegram!`")
        for nexa_aud in exted_aud:
            await message.reply_audio(audio=nexa_aud, caption=f"`Extracted by` {(await NEXAUB.get_me()).mention}")
        await ext_text.edit("`Extracting Finished!`")
        shutil.rmtree("./NexaUb" + "/" + "py_extract/audios")
    except Exception as e:
        await ext_text.edit(f"**Error:** `{e}`")
