# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os
import shutil

from aiohttp import ClientSession
from pyrogram.types import Message, InputMediaDocument

from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg, download_images
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Wallpaper,**

  ✘ `wall` - To get list of wallpapers according to the give query

**Example:**

  ✘ `wall`,
   ⤷ Send command with url = `{Config.CMD_PREFIX}wall cyberpunk`
   ⤷ Reply to a message = `{Config.CMD_PREFIX}wall`

  **Tip 💡,**
   ⤷ You can limit the results too. See below examples,
    ⤷ Send command with url = `{Config.CMD_PREFIX}wall 5 cyberpunk`
    ⤷ Reply to a message = `{Config.CMD_PREFIX}wall 5`
""",
        f"{mod_name}_category": "tools"
    }
)


# Function to get wallpapers link from "r/wallpaper" subreddit
async def fetch_wallpapers(query, limit=10):
    actual_limit = limit if limit <= 20 else 10
    url = f"https://nexa-apis.herokuapp.com/reddit?query={query}&subreddit=wallpaper"
    wall_list = []
    async with ClientSession() as wall_client:
        getit = await wall_client.get(url)
        jsn = await getit.json()
        if not jsn["status"] == "Ok":
            return wall_list
        # Adding the image urls to the list
        for wall in jsn["data"]:
            if not len(wall_list) >= actual_limit:
                img = wall["image"]
                if img:
                    wall_list.append(img)
        return wall_list

# Function to make input media list
async def make_input_media_list(image_paths: list):
    input_media_list = []
    for path in image_paths:
        input_media_list.append(
            InputMediaDocument(path, caption=f"**Uploaded with ✨ Nexa Userbot!**")
        )
    return input_media_list


@nexaub.on_cmd(command=["wall", "wallpaper"])
async def gib_wallpapers(_, message: Message):
    wall_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    args = get_arg(message)
    # Defalut limit
    limit = 10
    if r_msg:
        if not r_msg.text:
            return await wall_msg.edit("`Give something to search!`")
        if args:
            limit = int(args)
        query = r_msg.text
    elif args:
        splitted = args.split(" ", 1)
        if len(splitted) >= 2:
            if splitted[0].isnumeric():
                limit = int(splitted[0])
            query = splitted[1]
        else:
            query = splitted[0]
    else:
        return await wall_msg.edit("`Give something to search!`")
    # Fetching the wallpapers from reddit api or Nexa-APis
    await wall_msg.edit("`Fetching wallpapers from the API...`")
    fetch_walls = await fetch_wallpapers(query, limit)
    if not fetch_walls:
        return await wall_msg.edit("`Ooops, Nothing found!`")
    # Downloading the wallpapers
    await wall_msg.edit("`Downloading the wallpapers. This may take a while! Until then go and drink some coffee ☕`")
    downld_walls = await download_images(fetch_walls)
    if not fetch_walls:
        return await wall_msg.edit("`Ooops, Download failed!`")
    # Uploading the wallpapers
    media_list = await make_input_media_list(downld_walls)
    await wall_msg.edit("`Uploading the wallpapers. This may take a while! Until then go and drink some coffee ☕`")
    # Splitting list if the lenght is greater than 10
    full_wall_list = []
    if len(media_list) >= 10:
        full_wall_list.append(media_list[:10])
        full_wall_list.append(media_list[10:])
    if full_wall_list:
        for spl_list in full_wall_list:
            await wall_msg.reply_media_group(spl_list)
    else:
        await wall_msg.reply_media_group(media_list)
    await wall_msg.delete()
    shutil.rmtree("cache/NEXAUB_Image_Downloader")