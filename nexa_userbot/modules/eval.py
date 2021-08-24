# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot

import traceback
import sys
import os
import re
import subprocess
from io import StringIO

from nexa_userbot import NEXAUB, CMD_HELP
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from config import Config


# Help
CMD_HELP.update(
    {
        "eval": f"""
**Eval**

  ✘ `eval` - To Run Pyrogram Evaluations
  ✘ `sh` - To Run commands in shell

**Example:**

  ✘ `eval`,
   ⤷ Send with pyrogram command = `{Config.CMD_PREFIX}eval await message.reply("Yo, wassup!")`

  ✘ `sh`,
   ⤷ Send with bash command = `{Config.CMD_PREFIX}sh pip3 install cowsay`
"""
    }
)

mod_file = os.path.basename(__file__)


async def aexec(code, client, message):
    exec(
        f"async def __aexec(client, message): "
        + "".join(f"\n {l}" for l in code.split("\n"))
    )
    return await locals()["__aexec"](client, message)


@nexaub_on_cmd(command="eval", modlue=mod_file)
async def evaluate(client, message):
    status_message = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await status_message.delete()
        return
    reply_to_id = message.message_id
    if message.reply_to_message:
        reply_to_id = message.reply_to_message.message_id
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, message)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**► Command:** \n`{cmd}` \n\n**► Response / Output:** \n`{evaluation.strip()}`"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(final_output))
        await NEXAUB.send_document(
            chat_id=message.chat.id,
            document=filename,
            caption=cmd,
            disable_notification=True,
            reply_to_message_id=reply_to_id,
        )
        os.remove(filename)
        await status_message.delete()
    else:
        await e_or_r(nexaub_message=status_message, msg_text=final_output)


@nexaub_on_cmd(command="sh", modlue=mod_file)
async def terminal(client, message):
    sh_eval_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    if len(message.text.split()) == 1:
        await sh_eval_msg.edit(f"`Invalid Command!` \n\n**Example:** `{Config.CMD_PREFIX}sh echo Hello World`")
        return
    try:
        cmd = message.text.split(" ", maxsplit=1)[1]
    except IndexError:
        await message.delete()
        return
    args = message.text.split(None, 1)
    teks = args[1]
    if "\n" in teks:
        code = teks.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
                )
            except Exception as err:
                print(err)
                await sh_eval_msg.edit(
                    """
**► Error:**
```{}```
""".format(
                        err
                    )
                )
            output += "**{}**\n".format(code)
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", teks)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
        except Exception as err:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type, value=exc_obj, tb=exc_tb
            )
            await sh_eval_msg.edit("""**► Error:**\n```{}```""".format("".join(errors)))
            return
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await client.send_document(
                message.chat.id,
                "output.txt",
                reply_to_message_id=message.message_id,
                caption="`Output file`",
            )
            os.remove("output.txt")
            return
        await sh_eval_msg.edit(f"**► Input:** \n`{cmd}` \n\n**► Output:**\n```{output}```", parse_mode="markdown")
    else:
        await sh_eval_msg.edit(f"**► Input:** \n`{cmd}` \n\n**► Output:**\n`No Output`")
