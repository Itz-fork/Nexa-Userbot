# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Ultroid Userbot | TeamUltroid

from telethon import events
from telethon.events import NewMessage
from telethon.tl.types import Channel, User, Chat
from telethon.tl.custom import Dialog
from telethon_ub import NEXAUB
from config import Config

@NEXAUB.on(events.NewMessage(outgoing=True, pattern=f"{Config.CMD_PREFIX}status"))
async def stats(
    event: NewMessage.Event,
) -> None:
    ok = await event.edit("`Processing...`")
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in NEXAUB.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel):
            if entity.broadcast:
                broadcast_channels += 1
                if entity.creator or entity.admin_rights:
                    admin_in_broadcast_channels += 1
                if entity.creator:
                    creator_in_channels += 1

            elif entity.megagroup:
                groups += 1
                if entity.creator or entity.admin_rights:
                    admin_in_groups += 1
                if entity.creator:
                    creator_in_groups += 1

        elif isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1

        elif isinstance(entity, Chat):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1

        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count

    owned_user = await NEXAUB.get_me()
    response = f"**Telegram Status of @{owned_user.username},** \n\n\n"
    response += f"**✦ Total Private Chats:** `{private_chats}` \n"
    response += f"        Users: `{private_chats - bots}` \n"
    response += f"        Bots: `{bots}` \n\n"
    response += f"**✦ Total Groups:** `{groups}` \n"
    response += f"        Creator: `{creator_in_groups}` \n"
    response += f"        Admin in: `{admin_in_groups}` \n"
    response += f"        Only Admin Rights: `{admin_in_groups - creator_in_groups}` \n\n"
    response += f"**✦ Total Channels:** `{broadcast_channels}` \n"
    response += f"        Creator: `{creator_in_channels}` \n"
    response += f"        Admin in: `{admin_in_broadcast_channels}` \n"
    response += f"        Only Admin Rights: `{admin_in_broadcast_channels - creator_in_channels}` \n\n"
    response += f"**✦ Unread:** \n"
    response += f"        Chats: `{unread}` \n"
    response += f"        Mentions: `{unread_mentions}` \n\n"
    await ok.edit(response)