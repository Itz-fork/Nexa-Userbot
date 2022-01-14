# Copyright (c) 2021 Itz-fork
# Part of: Nexa Userbot
import os

from aiohttp import ClientSession
from aiofiles import open as openfile
from asyncio import sleep
from .pyrogram_help import humanbytes


class NexaDL:
    """
    ## NexaDL

        Downloads files from direct links using aiohttp
    
    ### Methods

        ``download`` - Function to download the file

    ### Arguments

        ``chunk_size`` - Custom chunk size (Default to 1024 * 6)
    """

    def __init__(self) -> None:
        self.path = "cache/NexaDL"
        self.chunk_size = 1024 * 1024
        self.stat_txt = """
**File Name:** `{name}`

**File Size:** `{size}`

**Progress:** `{downloaded}` of `{total}`

`{prgs_bar}`

**Status:** `Downloading...`
"""
    
    async def download(self, url, message, path=None):
        """
        ## Arguments

            ``url`` - Url to download

            ``message`` - Pyrogram message object
            
            ``path`` (optional) - Path
        """
        name = await self._get_file_name(url)
        await self._make_dir(path)
        if not path:
            fpath = f"{self.path}/{name}"
        else:
            fpath = f"{path}/{name}"
        downloaded = 0
        async with ClientSession() as session:
            async with session.get(url, timeout=None) as resp:
                fs = int(resp.headers.get("Content-Length"))
                async with openfile(fpath, mode="wb") as file:
                    async for chunk in resp.content.iter_chunked(self.chunk_size):
                        await file.write(chunk)
                        downloaded += len(chunk)
                        done = int(15 * downloaded / fs)
                        try:
                            await message.edit(self.stat_txt.format(
                                name=name,
                                size=humanbytes(fs),
                                downloaded=humanbytes(downloaded),
                                total=humanbytes(fs),
                                prgs_bar="[%s%s]" % ("▰" * done, "▱" * (15-done))
                                )
                            )
                            await sleep(0.1)
                        except:
                            pass
        return fpath
    
    async def _get_file_name(self, url):
        return os.path.basename(url)
    
    async def _make_dir(self, path):
        if not path:
            if not os.path.isdir(self.path):
                os.makedirs(self.path)
        else:
            if not os.path.isdir(path):
                os.makedirs(path)