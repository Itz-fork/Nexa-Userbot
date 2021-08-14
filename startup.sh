instal_reqs () {
    echo "Installing Packages"
    apt-get update -y
    apt-get install -y megatools
  }

echo "
============ Nexa Userbot ============

Starting Now...
"

start_nexaub () {
    if [[ -z "$PYRO_STR_SESSION" ]]
    then
	    echo "Please add Pyrogram String Session"
    else
	    python -m pyrogram_ub
    fi
  }

_install_nexaub () {
    instal_reqs
    start_nexaub
  }
