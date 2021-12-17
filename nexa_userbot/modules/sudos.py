# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os

from pyrogram.types import Message
from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.nexaub_database.nexaub_db_conf import set_custom_var, get_custom_var, del_custom_var
from nexa_userbot.core.nexaub_database.nexaub_db_sudos import add_sudo, remove_sudo, check_if_sudo
from .ub_updater import restart_nexaub
from config import Config


# Help
CMD_HELP.update(
    {
        "sudos": f"""
**Sudos,**

  ✘ `setvar` - To Set a Variable
  ✘ `getvar` - To Get value of a variable
  ✘ `delvar` - To Delete a variable
  ✘ `addsudo` - To Add a Sudo User
  ✘ `rsudo` - To Remove a Sudo User

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
"""
    }
)

mod_file = os.path.basename(__file__)


@nexaub_on_cmd(command="addsudo", modlue=mod_file)
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
    await sudo_msg.edit(f"**Successfully Added New Sudo User** \n\n**User ID:** `{sudo_user_id}`")
    await restart_nexaub()
  else:
    await sudo_msg.edit("`Please give a valid user id to add as a sudo user`")


@nexaub_on_cmd(command="rsudo", modlue=mod_file)
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
    await sudo_msg.edit(f"**Successfully Removed Sudo User** \n\n**User ID:** `{sudo_user_id}`")
    await restart_nexaub()
  else:
    await sudo_msg.edit("`Please give a valid user id to add as a sudo user`")


@nexaub_on_cmd(command="setvar", modlue=mod_file)
async def setmongovar(_, message: Message):
  setvr_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  var_val = get_arg(message)
  if not var_val:
    return await setvr_msg.edit("`Give Variable and Value to set!`")
  else:
    s_var = var_val.split(" ", 1)
    await set_custom_var(var=s_var[0], value=s_var[1])
    await setvr_msg.edit(f"**Successfully Added Custom Var** \n\n**Var:** `{s_var[0]}` \n**Val:** `{s_var[1]}`")

@nexaub_on_cmd(command="getvar", modlue=mod_file)
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

@nexaub_on_cmd(command="delvar", modlue=mod_file)
async def del_var(_, message: Message):
  d_var = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  var_d = get_arg(message)
  if not var_d:
    return await d_var.edit("`Give Variable to delete!`")
  else:
    deld_var = await del_custom_var(var_d)
    if deld_var:
      await d_var.edit(f"**Successfully Deleted** `{var_d}` **Var from database!**")


@nexaub_on_cmd(command="add_plugin_channel", modlue=mod_file)
async def add_custom_plugin_channel(_, message: Message):
  acpc = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  get_c_name = get_arg(message)
  if not get_c_name:
    return await acpc.edit("`Give a channel username to add it as a custom plugin channel!`")
  channel_username = get_c_name.replace("@", "")
  is_exists = await get_custom_var("CUSTOM_PLUGINS_CHANNELS")
  if is_exists:
    await set_custom_var("CUSTOM_PLUGINS_CHANNELS", is_exists.append(channel_username))
  else:
    await set_custom_var("CUSTOM_PLUGINS_CHANNELS", [channel_username])
  await acpc.edit(f"**Successfully Added Custom Plugin Channel** \n\n**Channel:** {get_c_name}")

@nexaub_on_cmd(command="rm_plugin_channel", modlue=mod_file)
async def remove_custom_plugin_channel(_, message: Message):
  rmcpc = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  rm_c_name = get_arg(message)
  if not rm_c_name:
    return await rmcpc.edit("`Give a channel username to remove it from custom plugin channel database!`")
  cstm_plgin_c = await get_custom_var("CUSTOM_PLUGINS_CHANNELS")
  if cstm_plgin_c and rm_c_name in cstm_plgin_c:
    new_custm_plgin_chnls = cstm_plgin_c.remove(rm_c_name)
    await set_custom_var("CUSTOM_PLUGINS_CHANNELS", new_custm_plgin_chnls)
    await rmcpc.edit(f"**Successfully Removed Custom Plugin Channel** \n\n**Channel:** {rm_c_name}")
  else:
    await rmcpc.edit("`First add custom plugin channel, then we can remove it :)`")