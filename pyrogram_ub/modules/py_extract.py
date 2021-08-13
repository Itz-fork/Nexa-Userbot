# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

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
    if not replied_msg:
        await ext_text.edit("`Please reply to a valid video file!`")
        return
    if not replied_msg.video:
        await ext_text.edit("`Please reply to a valid video file!`")
        return
    replied_video = replied_msg.video
    video_fname = f"NEXAUB_DOWNLOADS/{replied_video.file_name}"
    ext_video = await NEXAUB.download_media(file_name=video_fname)
    ext_audios = Video_tools.extract_all_audio(input_file=ext_video)
    for audio in ext_video:
        await NEXAUB.send_audio(chat_id=message.chat.id, audio=audio)
