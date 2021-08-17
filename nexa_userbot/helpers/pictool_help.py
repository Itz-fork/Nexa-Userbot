# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: TheHamkerCat

from io import BytesIO
from aiohttp import ClientSession


# Aiohttlp Session
aiosession = ClientSession()

async def gib_carbon_sar(code):
    url = "https://carbonara.vercel.app/api/cook"
    async with aiosession.post(url, json={"code": code}) as resp:
        image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image