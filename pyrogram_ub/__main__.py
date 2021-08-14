# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
import os
from pyrogram_ub import NEXAUB
from pyrogram_ub.modules import *
from config import Config

print("Pyrogram Client Has Started! \n\nPowered by Nexa UserBot")
if not os.path.isdir(Config.DOWNLOAD_LOCATION):
  os.makedirs(Config.DOWNLOAD_LOCATION)
NEXAUB.run()
