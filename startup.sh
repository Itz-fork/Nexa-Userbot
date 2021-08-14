echo "
============ Nexa Userbot ============

Starting Now...
"
apt install megatools

if [[ -z "$PYRO_STR_SESSION" ]]
then
	echo "Please add Pyrogram String Session"
else
	python -m pyrogram_ub
fi
