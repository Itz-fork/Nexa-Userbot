# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

from pyrogram.types import Message
from py_trans import Async_PyTranslator

from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from nexa_userbot.helpers.pyrogram_help import get_arg
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Translator (py-trans),**

  ✘ `ptr` - Translate text using 

**Example:**

   **Options:**

    ⤷ dest_lang = destination language (Required)
    ⤷ tr_engine = translation_engine (Optional) - [list here](https://github.com/Itz-fork/py-trans#supported-engines)
    ⤷ to_tr_text = Translate text (Required)

  ✘ `ptr`,

   ⤷ Reply to a text message with options,
    **Structure:**
        `{Config.CMD_PREFIX}ptr [dest_lang] [tr_engine]`
    **Ex:**
        `{Config.CMD_PREFIX}ptr si google`
    
   ⤷ Send with text with options,
    **Structure:**
        `{Config.CMD_PREFIX}ptr [dest_lang] [tr_engine] [to_tr_text]`
    **Ex:**
        `{Config.CMD_PREFIX}ptr si google Heya, I'm using telegram`
""",
        f"{mod_name}_category": "tools"
    }
)


@nexaub.on_cmd(command=["ptr"])
async def pytrans_tr(_, message: Message):
  tr_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
  r_msg = message.reply_to_message
  args = get_arg(message)
  if r_msg:
    if r_msg.text:
      to_tr = r_msg.text
    else:
      return await tr_msg.edit("`Reply to a message that contains text!`")
    # Checks if dest lang is defined by the user
    if not args:
      return await tr_msg.edit(f"`Please define a destination language!` \n\n**Ex:** `{Config.CMD_PREFIX}ptr si Hey, I'm using telegram!`")
    # Setting translation if provided
    else:
      sp_args = args.split(" ")
      if len(sp_args) == 2:
        dest_lang = sp_args[0]
        tr_engine = sp_args[1]
      else:
        dest_lang = sp_args[0]
        tr_engine = "google"
  elif args:
    # Splitting provided arguments in to a list
    a_conts = args.split(None, 2)
    # Checks if translation engine is defined by the user
    if len(a_conts) == 3:
      dest_lang = a_conts[0]
      tr_engine = a_conts[1]
      to_tr = a_conts[2]
    else:
      dest_lang = a_conts[0]
      to_tr = a_conts[1]
      tr_engine = "google"
  # Translate the text
  py_trans = Async_PyTranslator(provider=tr_engine)
  translation = await py_trans.translate(to_tr, dest_lang)
  # Parse the translation message
  if translation["status"] == "success":
    tred_txt = f"""
**Translation Engine**: `{translation["engine"]}`
**Translated to:** `{translation["dest_lang"]}`
**Translation:**
`{translation["translation"]}`
"""
    if len(tred_txt) > 4096:
      await tr_msg.edit("`Wah!! Translated Text So Long Tho!, Give me a minute, I'm sending it as a file!`")
      tr_txt_file = open("translated_NEXAUB.txt", "w+")
      tr_txt_file.write(tred_txt)
      tr_txt_file.close()
      await tr_msg.reply_document("ptranslated_NEXAUB.txt")
      os.remove("ptranslated_NEXAUB.txt")
      await tr_msg.delete()
    else:
      await tr_msg.edit(tred_txt)