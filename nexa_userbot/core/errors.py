# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

class Errors:
    """
    ## Errors

    ### Arguments:

        None
    """
    class SpamFailed(Exception):
        """
        Raises when the spam task was failed
        """
        pass

    class DownloadFailed(Exception):
        """
        Raises when the download task was failed
        """
        pass
    class DelAllFailed(Exception):
        """
        Raises when the del all function was failed
        """
        pass