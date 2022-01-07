# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot | Nexa Userbot

import os
import time
import json

from sys import version_info
from datetime import datetime
from pyrogram import __version__ as pyrogram_version
from pyrogram.types import Message

from nexa_userbot import NEXAUB, CMD_HELP, StartTime
from nexa_userbot.helpers.pyrogram_help import get_arg, convert_to_image
from nexa_userbot.core.nexaub_database.nexaub_db_conf import set_custom_alive_msg, get_custom_alive_msg, set_custom_var, get_custom_var
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from nexa_userbot.core.startup_checks import check_or_set_log_channel
from .Extras import get_xtra_modules_names
from .telegraph import upload_to_tgraph
from . import __all__ as all_mods
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Alive,**

  ✘ `alive` - To Check If Your Nexa Userbot Alive
  ✘ `ping` - To Check Ping Speed
  ✘ `setalive` - To Set Custom Alive Message
  ✘ `getalive` - To Get current alive message
  ✘ `setalivepic` - To Set Custom Alive Picture
  ✘ `getalivepic` - To Get Current Custom Alive Picture

**Example:**

  ✘ `setalive`,
   ⤷ Send with alive text = `{Config.CMD_PREFIX}setalive This is the alive text`
   ⤷ Reply to a text message with `{Config.CMD_PREFIX}setalive`

  ✘ `setalivepic`,
   ⤷ Reply to a picture/gif/sticker with `{Config.CMD_PREFIX}setalivepic` (Under 5MB)
""",
        f"{mod_name}_category": "userbot"
    }
)


# Get python version
python_version = f"{version_info[0]}.{version_info[1]}.{version_info[2]}"
# Conver time in to readable format
def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "
    time_list.reverse()
    ping_time += ":".join(time_list)
    return ping_time

# Get current version of Nexa Userbot
async def get_nexaub_version():
    with open("cache/nexaub_data.json", "r") as jsn_f:
        ver = json.load(jsn_f)
        return ver["version"]


# Alive Message
@nexaub.on_cmd(command=["alive"])
async def pyroalive(_, message: Message):
    uptime = get_readable_time((time.time() - StartTime))
    alive_bef_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    # Alive Message
    get_alive_msg = await get_custom_alive_msg()
    custom_alive_msg = get_alive_msg if get_alive_msg else "Heya, I'm Using Nexa Userbot"
    # Alive Pic
    g_al_pic = await get_custom_var(var="ALIVE_PIC")
    alive_pic = g_al_pic[1] if g_al_pic else "cache/NEXAUB.png"
    NEXAUB_VERSION = await get_nexaub_version()
    xtra_modules = await get_xtra_modules_names()
    alive_msg = f"""
**{custom_alive_msg}**


**✨ Nexa UserBot is Alive**
    
    **》 Nexa Userbot Version:** `{NEXAUB_VERSION}`
    **》 Python Version:** `{python_version}`
    **》 Pyrogram Version:** `{pyrogram_version}`
    **》 Uptime:** `{uptime}`
    **》 Loaded Plugins:** `{len(all_mods)}`
    **》 Loaded Custom Plugins:** `{len(xtra_modules)}`


**Deploy Your Own: @NexaBotsUpdates**"""
    await alive_bef_msg.delete()
    if g_al_pic and g_al_pic[0] == "gif":
        await NEXAUB.send_animation(chat_id=message.chat.id, animation=alive_pic, caption=alive_msg)
    else:
        await NEXAUB.send_photo(chat_id=message.chat.id, photo=alive_pic, caption=alive_msg)

# Ping
@nexaub.on_cmd(command=["ping"], group=-1)
async def pingme(_, message: Message):
    start = datetime.now()
    ping_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    end = datetime.now()
    ping_time = (end - start).microseconds / 1000
    await ping_msg.edit(f"**Pong:** `{ping_time} ms` \n\n ~ **✨ Nexa-Userbot**", disable_web_page_preview=True)

# Set custom alive message
@nexaub.on_cmd(command=["setalive"])
async def set_alive(_, message: Message):
    alive_r_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    c_alive_msg = get_arg(message)
    r_msg = message.reply_to_message
    if not c_alive_msg:
        if r_msg:
            c_alive_msg = r_msg.text
        else:
            return await alive_r_msg.edit("`Please reply to a text message!`")
    await set_custom_alive_msg(a_text=c_alive_msg)
    await alive_r_msg.edit("`Successfully Updated Custom Alive Message!`")

# Get custom alive message
@nexaub.on_cmd(command=["getalive"])
async def get_alive(_, message: Message):
    g_alive_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    try:
        get_al = await get_custom_alive_msg()
        saved_alive_msg = get_al if get_al else "No Custom Message is saved!"
        await g_alive_msg.edit(f"**Current Alive Message:** \n{saved_alive_msg}")
    except Exception as e:
        print(e)

# Set custom alive picture
@nexaub.on_cmd(command=["setalivepic"])
async def set_alive_pic(_, message: Message):
    cust_alive = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    r_msg = message.reply_to_message
    if r_msg.photo or r_msg.animation or r_msg.sticker:
        # Converts sticker into an image
        if r_msg.sticker:
            alive_pic = await convert_to_image(message=r_msg, client=NEXAUB)
        # Else it'll just download the photo/gif
        else:
            alive_pic = await r_msg.download()
        # Upload that shit to telegraph
        alive_url = await upload_to_tgraph(alive_pic)
        if r_msg.photo or r_msg.sticker:
            await set_custom_var(var="ALIVE_PIC", value=["photo", alive_url])
        else:
            await set_custom_var(var="ALIVE_PIC", value=["gif", alive_url])
        await cust_alive.edit(f"`Successfully Saved Custom Alive Picture!` \n\n**Preview:** [Click here]({alive_url})")
    else:
        await cust_alive.edit("`Reply to a photo, gif or sticker 😑!`")

# Get custom alive picture
@nexaub.on_cmd(command=["getalivepic"])
async def get_alive_pic(_, message: Message):
    get_pic_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    g_al_pic = await get_custom_var(var="ALIVE_PIC")
    if g_al_pic:
        picture = g_al_pic[1]
        ptype = g_al_pic[0]
        await get_pic_msg.delete()
        if ptype == "gif":
            await NEXAUB.send_animation(chat_id=message.chat.id, animation=picture, caption=f"**Nexa-Userbot's Custom Alive Picture** \n\n**Type:** `{ptype}`")
        else:
            await NEXAUB.send_photo(chat_id=message.chat.id, photo=picture, caption=f"**Nexa-Userbot's Custom Alive Picture** \n\n**Type:** `{ptype}`")
    else:
        await get_pic_msg.edit("`Save a custom alive picture first!`")


@nexaub.on_cmd(command=["clc"])
async def egg_clc(_, message: Message):
    clc_func = await check_or_set_log_channel()
    lc_id = clc_func[1] if clc_func[1]  else None
    await e_or_r(nexaub_message=message, msg_text=f"**Is Log Channel Set?** `{clc_func[0]}` \n**Channel ID:** `{lc_id}`")
