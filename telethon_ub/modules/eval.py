# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot | XDITYA

import io
import sys
import traceback

from telethon import events, TelegramClient
from telethon_ub import NEXAUB
from config import PREFIX


@NEXAUB.on(events.NewMessage(outgoing=True, pattern=f"^{PREFIX}teval (.*)"))
async def t_eval(event):
    if event.fwd_from:
        return
    await event.edit("`Processing...`")
    cmd = event.text.split(" ", maxsplit=1)[1]
    reply_to_id = event.message.id
    if event.reply_to_msg_id:
        reply_to_id = event.reply_to_msg_id

    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = io.StringIO()
    redirected_error = sys.stderr = io.StringIO()
    stdout, stderr, exc = None, None, None

    try:
        await aexec(cmd, event)
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

    final_output = "**► Command:**: \n`{}` \n\n**► Response / Output:** \n`{}` \n".format(
        cmd, evaluation
    )

    if len(final_output) > int("1024"):
        with io.BytesIO(str.encode(final_output)) as out_file:
            out_file.name = "telethon_eval.text"
            await event.client.send_file(
                event.chat_id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption="Telethon Eval",
                reply_to=reply_to_id,
            )
    else:
        await event.edit(final_output)


async def aexec(code, event):
    exec(f"async def __aexec(event): " + "".join(f"\n {l}" for l in code.split("\n")))
    return await locals()["__aexec"](event)