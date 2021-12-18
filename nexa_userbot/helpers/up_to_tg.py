# Copyright (c) 2021 Itz-fork
# Part of: Nexa Userbot
import os
import re
import filetype
from .pyrogram_help import run_shell_cmds

from nexa_userbot import NEXAUB

async def get_vid_duration(input_video):
    result = await run_shell_cmds(f"ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {input_video}")
    return int(result)

async def guess_and_send(input_file, chat_id, thumb_path):
    thumbnail_bpath = thumb_path
    in_file = f"{input_file}"
    guessedfilemime = filetype.guess(in_file)
    if not guessedfilemime or not guessedfilemime.mime:
        return await NEXAUB.send_document(chat_id=chat_id, document=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
    try:
        filemimespotted = guessedfilemime.mime
        # For gifs
        if re.search(r'\bimage/gif\b', filemimespotted):
            await NEXAUB.send_animation(chat_id=chat_id, animation=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
        # For images
        elif re.search(r'\bimage\b', filemimespotted):
            await NEXAUB.send_photo(chat_id=chat_id, photo=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
        # For videos
        elif re.search(r'\bvideo\b', filemimespotted):
            viddura = await get_vid_duration(input_video=in_file)
            thumbnail_path = f"{thumbnail_bpath}/thumbnail_{os.path.basename(in_file)}.jpg"
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            await run_shell_cmds(f"ffmpeg -i {in_file} -ss 00:00:01.000 -vframes 1 {thumbnail_path}")
            await NEXAUB.send_video(chat_id=chat_id, video=in_file, duration=viddura, thumb=thumbnail_path, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
        # For audio
        elif re.search(r'\baudio\b', filemimespotted):
            await NEXAUB.send_audio(chat_id=chat_id, audio=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
        else:
            await NEXAUB.send_document(chat_id=chat_id, document=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
    except Exception as e:
        print(e)
        await NEXAUB.send_document(chat_id=chat_id, document=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")