# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot

import glob
from os.path import dirname, basename, isfile, join

async def get_xtra_modules_names():
    modules = glob.glob(join(dirname(__file__), "*.py"))
    __xall__ = [
        basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
    ]
    return __xall__