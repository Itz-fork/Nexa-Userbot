# Copyright (c) 2021 Itz-fork
# Part of: Nexa Userbot
import os
import filetype
import subprocess

from nexa_userbot import NEXAUB

def get_vid_duration(input_video):
    result = subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

async def guess_and_send(input_file, chat_id, thumb_path):
    chat_id = chat_id
    thumbnail_bpath = thumb_path
    in_file = f"{input_file}"
    guessedfilemime = filetype.guess(in_file)
#     if not guessedfilemime.mime:
#         await NEXAUB.send_document(chat_id=chat_id, document=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
#         return
    try:
        filemimespotted = guessedfilemime.mime
        if "image/gif" in filemimespotted:
            await NEXAUB.send_animation(chat_id=chat_id, animation=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
        elif "image" in filemimespotted:
            await NEXAUB.send_photo(chat_id=chat_id, photo=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
        elif "video" in filemimespotted:
            viddura = get_vid_duration(input_video=in_file)
            thumbnail_path = f"{thumbnail_bpath}/thumbnail.jpg"
            if os.path.exists(thumbnail_path):
                os.remove(thumbnail_path)
            cmd = f"ffmpeg -i {in_file} -ss 00:00:01.000 -vframes 1 {thumbnail_path}"
            subprocess.run(cmd, shell=True)
            await NEXAUB.send_video(chat_id=chat_id, video=in_file, duration=viddura, thumb=thumbnail_path, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
        elif "audio" in filemimespotted:
            await NEXAUB.send_audio(chat_id=chat_id, audio=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
        else:
            await NEXAUB.send_document(chat_id=chat_id, document=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
    except Exception as e:
        print(e)
        await NEXAUB.send_animation(chat_id=chat_id, animation=in_file, caption=f"`Uploaded by` {(await NEXAUB.get_me()).mention}")
