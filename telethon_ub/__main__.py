# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot

import sys
import glob
import logging
import importlib
from pathlib import Path
from telethon import TelegramClient, events
from telethon_ub import NEXAUB
from telethon_ub.modules import *

def load_plugins(plugin_name):
    path = Path(f"telethon_ub/modules/{plugin_name}.py")
    name = "telethon_ub.modules.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["telethon_ub.modules." + plugin_name] = load

path = "telethon_ub/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

NEXAUB.start()
print("Telethon Client Has Started! \n\nPowered by Nexa UserBot")
NEXAUB.run_until_disconnected()