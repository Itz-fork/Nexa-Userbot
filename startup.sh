#!/usr/bin/bash

start_nexaub () {
  if [[ -z "$PYRO_STR_SESSION" ]]
  then
    echo "Please add Pyrogram String Session"
  else
	  python3 -m nexa_userbot
  fi
}

_install_nexaub () {
  echo ">>>> Starting Nexa-Userbot"
  start_nexaub
  echo "
============ Nexa Userbot ============


Copyright (c) 2021 Itz-fork | @NexaBotsUpdates
  "
}

_install_nexaub