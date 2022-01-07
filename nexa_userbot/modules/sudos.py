# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os

from pyrogram.types import Message
from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.nexaub_database.nexaub_db_conf import set_custom_var, get_custom_var, del_custom_var
from nexa_userbot.core.nexaub_database.nexaub_db_sudos import add_sudo, remove_sudo, check_if_sudo, add_custom_plugin_channel, get_custom_plugin_channels, remove_custom_plugin_channel
from .updater import restart_nexaub
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Sudos,**

  ✘ `setvar` - To Set a Variable
  ✘ `getvar` - To Get value of a variable
  ✘ `delvar` - To Delete a variable
  ✘ `addsudo` - To Add a Sudo User
  ✘ `rsudo` - To Remove a Sudo User
  ✘ `add_plugin_channel` - To Add Custom Plugin Channel
  ✘ `rm_plugin_channel` - To Remove Custom Plugin Channel
  ✘ `get_plugin_channels` - To Get Custom Plugin Channels

**Example:**

  ✘ `setvar`,
   ⤷ Send command with Var and Value = `{Config.CMD_PREFIX}setvar YOUR_VAR your_value`

  ✘ `getvar`,
   ⤷ Send command with Var = `{Config.CMD_PREFIX}getvar YOUR_VAR`

  ✘ `delvar`,
   ⤷ Send command with Var = `{Config.CMD_PREFIX}delvar YOUR_VAR`

  ✘ `addsudo`,
   ⤷ Send command with user id = `{Config.CMD_PREFIX}addsudo 1234567`
   ⤷ Reply to a user message = `{Config.CMD_PREFIX}addsudo` (Reply to a user message)

  ✘ `rsudo`,
   ⤷ Send command with sudo user id = `{Config.CMD_PREFIX}rsudo 1234567`
   ⤷ Reply to a sudo user message = `{Config.CMD_PREFIX}rsudo` (Reply to a user message)
""",
        f"{mod_name}_category": "utils"
    }
)


@nexaub.on_cmd(command=["addsudo"])
async def set_sudo(_, message: Message):
  sudo_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  sudo_id = str(get_arg(message))
  r_sudo_msg = message.reply_to_message
  if r_sudo_msg:
    sudo_user_id = str(r_sudo_msg.from_user.id)
  else:
    sudo_user_id = str(sudo_id)
  is_sudo = await check_if_sudo(sudo_user_id)
  if is_sudo is True:
    await sudo_msg.edit(f"**User** `{sudo_user_id}` **is already a sudo user**")
    return
  else:
    pass
  is_id_ok = sudo_user_id.isnumeric()
  if is_id_ok is True:
    await add_sudo(sudo_user_id)
    await sudo_msg.edit(f"**Successfully Added New Sudo User** \n\n**User ID:** `{sudo_user_id}` \n\nRestarting your bot to apply the changes!")
    await restart_nexaub()
  else:
    await sudo_msg.edit("`Please give a valid user id to add as a sudo user`")


@nexaub.on_cmd(command=["rsudo"])
async def set_sudo(_, message: Message):
  sudo_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  sudo_id = str(get_arg(message))
  r_sudo_msg = message.reply_to_message
  if r_sudo_msg:
    sudo_user_id = str(r_sudo_msg.from_user.id)
  else:
    sudo_user_id = str(sudo_id)
  is_sudo = await check_if_sudo(sudo_user_id)
  if is_sudo is False:
    await sudo_msg.edit(f"**User** `{sudo_user_id}` **isn't a sudo user lol!**")
    return
  else:
    pass
  is_id_ok = sudo_user_id.isnumeric()
  if is_id_ok is True:
    await remove_sudo(sudo_user_id)
    await sudo_msg.edit(f"**Successfully Removed Sudo User** \n\n**User ID:** `{sudo_user_id}` \n\nRestarting your bot to apply the changes!")
    await restart_nexaub()
  else:
    await sudo_msg.edit("`Please give a valid user id to add as a sudo user`")


@nexaub.on_cmd(command=["setvar"])
async def setmongovar(_, message: Message):
  setvr_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  var_val = get_arg(message)
  if not var_val:
    return await setvr_msg.edit("`Give Variable and Value to set!`")
  else:
    s_var = var_val.split(" ", 1)
    await set_custom_var(var=s_var[0], value=s_var[1])
    await setvr_msg.edit(f"**Successfully Added Custom Var** \n\n**Var:** `{s_var[0]}` \n**Val:** `{s_var[1]}`")

@nexaub.on_cmd(command=["getvar"])
async def get_var(_, message: Message):
  g_var = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  var_g = get_arg(message)
  if not var_g:
    return await g_var.edit("`Give Variable and Value to set!`")
  else:
    g_var_s = await get_custom_var(var=var_g)
    if g_var_s is None:
      return await g_var.edit("`Is that var exists?`")
    else:
      await g_var.edit(f"**Var:** `{var_g}` \n**Val:** `{g_var_s}`")

@nexaub.on_cmd(command=["delvar"])
async def del_var(_, message: Message):
  d_var = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  var_d = get_arg(message)
  if not var_d:
    return await d_var.edit("`Give Variable to delete!`")
  else:
    deld_var = await del_custom_var(var_d)
    if deld_var:
      await d_var.edit(f"**Successfully Deleted** `{var_d}` **Var from database!**")


@nexaub.on_cmd(command=["add_plugin_channel", "a_p_c", "add_plugins"])
async def add_custom_plug(_, message: Message):
  acpc = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  get_c_name = get_arg(message)
  if not get_c_name:
    return await acpc.edit("`Give a channel username to add it as a custom plugin channel!`")
  if get_c_name.isnumeric():
    plug_channel = int(get_c_name)
  else:
    plug_channel = get_c_name.replace("@", "")
  custp_list = await get_custom_plugin_channels()
  if plug_channel in custp_list:
    return await acpc.edit("`Channel is already added!`")
  await add_custom_plugin_channel(plug_channel)
  await acpc.edit(f"**Successfully Added Custom Plugin Channel** \n\n**Channel:** {get_c_name}")

@nexaub.on_cmd(command=["rm_plugin_channel", "rm_c", "rm_plugins"])
async def remove_custom_plug(_, message: Message):
  rmcpc = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  rm_c_name = get_arg(message)
  if not rm_c_name:
    return await rmcpc.edit("`Give a channel username to remove it from custom plugin channel database!`")
  custp_list = await get_custom_plugin_channels()
  if rm_c_name not in custp_list:
    await rmcpc.edit("`First add custom plugin channel, then we can remove it :)`")
  await remove_custom_plugin_channel(rm_c_name)
  await rmcpc.edit(f"**Successfully Removed Custom Plugin Channel** \n\n**Channel:** {rm_c_name}")

@nexaub.on_cmd(command=["get_plugin_channels", "get_c", "get_plugins"])
async def get_custom_plug(_, message: Message):
  getcpc = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  channel_list = await get_custom_plugin_channels()
  if not channel_list:
    return await getcpc.edit("`Add some custom plugin channels!`")
  channel_str = "**Available Custom Plugin Channels!** \n\n"
  for ch in channel_list:
    channel_str += f" ➥ `{ch}` \n"
  await getcpc.edit(channel_str)