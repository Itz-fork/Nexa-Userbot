# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import asyncio
import tgcrypto
from pyrogram import Client

print("""
    _   __                   __  __               __          __ 
   / | / /__  _  ______ _   / / / /_______  _____/ /_  ____  / /_
  /  |/ / _ \| |/_/ __ `/  / / / / ___/ _ \/ ___/ __ \/ __ \/ __/
 / /|  /  __/>  </ /_/ /  / /_/ (__  )  __/ /  / /_/ / /_/ / /_  
/_/ |_/\___/_/|_|\__,_/   \____/____/\___/_/  /_.___/\____/\__/ 

Copyright (c) 2021 Itz-fork | Nexa Userbot
""")

async def pyro_str():
    print("\nPlease Enter All Required Values to Generate Pyrogram String Session for your Account! \n")
    api_id = int(input("Enter Your APP ID: "))
    api_hash = input("Enter Your API HASH: ")
    async with Client(":memory:", api_id, api_hash) as NEXAUB:
        pyro_session = await NEXAUB.export_session_string()
        session_msg = await NEXAUB.send_message("me", f"`{pyro_session}`")
        await session_msg.reply_text("Successfully Generated String Session! Thanks for trying [Nexa Userbot](https://github.com/Itz-fork/Nexa-Userbot) \n\n**Join @NexaBotsUpdates**", disable_web_page_preview=True)

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(pyro_str())
