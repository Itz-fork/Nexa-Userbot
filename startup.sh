echo "
    _   __                   __  __               __          __ 
   / | / /__  _  ______ _   / / / /_______  _____/ /_  ____  / /_
  /  |/ / _ \| |/_/ __ `/  / / / / ___/ _ \/ ___/ __ \/ __ \/ __/
 / /|  /  __/>  </ /_/ /  / /_/ (__  )  __/ /  / /_/ / /_/ / /_  
/_/ |_/\___/_/|_|\__,_/   \____/____/\___/_/  /_.___/\____/\__/  

Starting Now....
"

if [[ -z "$PYRO_STR_SESSION" ]]
then
	echo "Please add Pyrogram String Session"
else
	python -m pyrogram_ub
fi
