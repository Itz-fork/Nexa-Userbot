# Copyright (c) 2021 Itz-fork
# Part of: Nexa Userbot
from pySmartDL import SmartDL
from pySmartDL.utils import get_filesize

class Downloader:
    """
    Downloads files from direct links using PySmartDL
    """

    def __init__(self, path=None) -> None:
        self.path = "cache/PYSmortDL" if not path else str(path)

    async def download(self, url):
        down_obj = SmartDL(url, dest=self.path, progress_bar=False)
        down_obj.start(blocking=False)
        return down_obj
    
    async def _isFinished(self, dl_obj):
        return dl_obj.isFinished()
    
    async def _isSuccess(self, dl_obj):
        return dl_obj.isSuccessful()
    
    async def _get_downloaded_file_details(self, dl_obj):
        # Checks if the downloading process was successful
        if not await self.__isSuccess(dl_obj):
            return
        dl_details = {}
        dl_details["path"] = dl_obj.get_dest()
        dl_details["time"] = dl_obj.get_dl_time(human=True)
        dl_details["md5"] = dl_obj.get_data_hash("md5")
        dl_details["sha1"] = dl_obj.get_data_hash("sha1")
        dl_details["sha256"] = dl_obj.get_data_hash("sha256")
        return dl_details

    async def _get_progress_details(self, dl_obj):
        details = {}
        details["speed"] = dl_obj.get_speed(human=True)
        details["downloaded"] = dl_obj.get_dl_size(human=True)
        details["eta"] = dl_obj.get_eta(human=True)
        details["progress"] = (dl_obj.get_progress()*100)
        details["status"] = dl_obj.get_status()
        return details