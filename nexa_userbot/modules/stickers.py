# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Friday Userbot | DevsExpo

import asyncio
import math
import shutil
import datetime
import zipfile
import os

from collections import defaultdict
from io import BytesIO
from PIL import Image
from pyrogram import filters, emoji
from pyrogram.errors import StickersetInvalid, YouBlockedUser
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName

from nexa_userbot import NEXAUB, CMD_HELP
from config import Config
from nexa_userbot.helpers.pyrogram_help import get_arg, convert_to_image
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r


# Help
CMD_HELP.update(
    {
        "stickers": f"""
**Stickers,**

  ✘ `packinfo` - To Get Information about a Sticker Pack
  ✘ `kang` - To kang a Sticker

**Example:**

  ✘ `packinfo`,
   ⤷ Reply to a sticker = `{Config.CMD_PREFIX}packinfo` (Reply to a sticker)

  ✘ `kang`,
   ⤷ Reply to a sticker = `{Config.CMD_PREFIX}kang` (Reply to a sticker)
"""
    }
)

mod_file = os.path.basename(__file__)

@nexaub_on_cmd(command="packinfo", modlue=mod_file)
async def packinfo(client, message):
    pablo = await e_or_r(nexaub_message=message, msg_text="Processing...")
    if not message.reply_to_message:
        await pablo.edit("`Please Reply to a Sticker!`")
        return
    if not message.reply_to_message.sticker:
        await pablo.edit("`Please Reply to a Sticker!`")
        return
    if not message.reply_to_message.sticker.set_name:
        await pablo.delete()
        return
    stickerset = await client.send(
        GetStickerSet(
            stickerset=InputStickerSetShortName(
                short_name=message.reply_to_message.sticker.set_name
            )
        )
    )
    emojis = []
    for stucker in stickerset.packs:
        if stucker.emoticon not in emojis:
            emojis.append(stucker.emoticon)
    output = f"""**Sticker Pack Title **: `{stickerset.set.title}`
**Sticker Pack Short Name:** `{stickerset.set.short_name}`
**Stickers Count:** `{stickerset.set.count}`
**Archived:** `{stickerset.set.archived}`
**Official:** `{stickerset.set.official}`
**Masks:** `{stickerset.set.masks}`
**Animated:** `{stickerset.set.animated}`
**Emojis In Pack:** `{' '.join(emojis)}`
"""
    await pablo.edit(output)


@nexaub_on_cmd(command="kang", modlue=mod_file)
async def kang_stick(client, message):
    pablo = await e_or_r(nexaub_message=message, msg_text="`Kanging This Sticker to My Pack...`")
    if not message.reply_to_message:
        await pablo.edit("`Please Reply to a Sticker!`")
        return
    Hell = get_arg(message)
    name = ""
    pack = 1
    nm = message.from_user.username
    if nm:
        nam = message.from_user.username
        name = nam[1:]
    else:
        name = message.from_user.first_name
    packname = f"@{nm} Kang Pack {pack}"
    packshortname = f"NEXAUB_{message.from_user.id}_{pack}"
    non = [None, "None"]
    emoji = "🤔"
    try:
        Hell = Hell.strip()
        if not Hell.isalpha():
            if not Hell.isnumeric():
                emoji = Hell
        else:
            emoji = "🤔"
    except:
        emoji = "🤔"
    exist = None
    is_anim = False
    if message.reply_to_message.sticker:
        if not Hell:
            emoji = message.reply_to_message.sticker.emoji or "🤔"
        is_anim = message.reply_to_message.sticker.is_animated
        if is_anim:
            packshortname += "_animated"
            packname += " Animated"
        if message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
        else:
            cool = await convert_to_image(message, client)
            if not cool:
                await pablo.edit("**Error:** `Unsupported Media`")
                return
            file_name = resize_image(cool)
    elif message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == "application/x-tgsticker":
            is_anim = True
            packshortname += "_animated"
            packname += " Animated"
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
    else:
        cool = await convert_to_image(message, client)
        if not cool:
            await pablo.edit("**Error:** `Unsupported Media`")
            return
        file_name = resize_image(cool)
    try:
        exist = await client.send(
            GetStickerSet(stickerset=InputStickerSetShortName(short_name=packshortname))
        )
    except StickersetInvalid:
        pass
    if exist:
        try:
            await client.send_message("stickers", "/addsticker")
        except YouBlockedUser:
            await pablo.edit("`Please Unblock @Stickers!`")
            await client.unblock_user("stickers")
        await client.send_message("stickers", packshortname)
        await asyncio.sleep(0.2)
        limit = "50" if is_anim else "120"
        messi = (await client.get_history("stickers", 1))[0]
        while limit in messi.text:
            pack += 1
            prev_pack = int(pack) - 1
            await pablo.edit("He he, Kang Pack Number `{}` is Full Of Stickers! Now Switching to `{}` Pack!".format(prev_pack, pack))
            packname = f"@{nm} Kang Pack {pack}"
            packshortname = f"NEXAUB_{message.from_user.id}_{pack}"
            if is_anim:
                packshortname += "_animated"
                packname += " Animated"
            await client.send_message("stickers", packshortname)
            await asyncio.sleep(0.2)
            messi = (await client.get_history("stickers", 1))[0]
            if messi.text == "Invalid pack selected.":
                if is_anim:
                    await client.send_message("stickers", "/newanimated")
                else:
                    await client.send_message("stickers", "/newpack")
                await asyncio.sleep(0.5)
                await client.send_message("stickers", packname)
                await asyncio.sleep(0.2)
                await client.send_document("stickers", file_name)
                await asyncio.sleep(1)
                await client.send_message("stickers", emoji)
                await asyncio.sleep(0.8)
                await client.send_message("stickers", "/publish")
                if is_anim:
                    await client.send_message("stickers", f"<{packname}>")
                await client.send_message("stickers", "/skip")
                await asyncio.sleep(0.5)
                await client.send_message("stickers", packshortname)
                await pablo.edit("**Sticker Kanged!** \n\n**Emoji:** {} \n**Pack:** [Here](https://t.me/addstickers/{})".format(emoji, packshortname))
                return
        await client.send_document("stickers", file_name)
        await asyncio.sleep(1)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(0.5)
        await client.send_message("stickers", "/done")
        await pablo.edit("**Sticker Kanged!** \n\n**Emoji:** {} \n**Pack:** [Here](https://t.me/addstickers/{})".format(emoji, packshortname))
    else:
        if is_anim:
            await client.send_message("stickers", "/newanimated")
        else:
            await client.send_message("stickers", "/newpack")
        await client.send_message("stickers", packname)
        await asyncio.sleep(0.2)
        await client.send_document("stickers", file_name)
        await asyncio.sleep(1)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(0.5)
        await client.send_message("stickers", "/publish")
        await asyncio.sleep(0.5)
        if is_anim:
            await client.send_message("stickers", f"<{packname}>")
        await client.send_message("stickers", "/skip")
        await asyncio.sleep(0.5)
        await client.send_message("stickers", packshortname)
        await pablo.edit("**Sticker Kanged!** \n\n**Emoji:** {} \n**Pack:** [Here](https://t.me/addstickers/{})".format(emoji, packshortname))
        try:
            if os.path.exists("Kanged_Sticker_NEXAUB.png"):
                os.remove("Kanged_Sticker_NEXAUB.png")
            downname = "./downloads"
            if os.path.isdir(downname):
                shutil.rmtree(downname)
        except:
            print("Can't remove downloaded sticker files")
            return


def resize_image(image):
    im = Image.open(image)
    maxsize = (512, 512)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        im.thumbnail(maxsize)
    file_name = "Kanged_Sticker_NEXAUB.png"
    im.save(file_name, "PNG")
    if os.path.exists(image):
        os.remove(image)
    return file_name
