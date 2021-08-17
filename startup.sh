echo "
============ Nexa Userbot ============

Starting Now...

Copyright (c) 2021 Itz-fork | @NexaBotsUpdates
"

start_nexaub () {
    if [[ -z "$PYRO_STR_SESSION" ]]
    then
	    echo "Please add Pyrogram String Session"
    else
	    python3 -m nexa_userbot
    fi
  }

_install_nexaub () {
    start_nexaub
  }

_install_nexaub