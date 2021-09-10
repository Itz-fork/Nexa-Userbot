# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os

from pyrogram.types import Message
from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.nexaub_database.nexaub_db_conf import set_custom_var, get_custom_var
from nexa_userbot.core.nexaub_database.nexaub_db_sudos import add_sudo, remove_sudo, check_if_sudo
from .ub_updater import restart_nexaub
from config import Config


# Help
CMD_HELP.update(
    {
        "sudos": f"""
**Sudos,**

  ✘ `setvar` - To Set a Variable
  ✘ `getvar` - To Get a Variable (val)
  ✘ `addsudo` - To Add a Sudo User
  ✘ `rsudo` - To Remove a Sudo User

**Example:**

  ✘ `setvar`,
   ⤷ Send command with Var and Value = `{Config.CMD_PREFIX}setvar YOUR_VAR your_value`

  ✘ `getvar`,
   ⤷ Send command with Var = `{Config.CMD_PREFIX}getvar YOUR_VAR`

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
    s_var = var_val.split(" ")
    variable, value = s_var 
    await set_custom_var(var=variable, value=value)
    await setvr_msg.edit(f"**Successfully Added Custom Var** \n\n**Var:** `{variable}` \n**Val:** `{value}`")

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
