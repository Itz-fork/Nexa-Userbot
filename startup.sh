echo "
============ Nexa Userbot ============

Starting Now...
"
apt -qq install -y --no-install-recommends megatools

if [[ -z "$PYRO_STR_SESSION" ]]
then
	echo "Please add Pyrogram String Session"
else
	python -m pyrogram_ub
fi
