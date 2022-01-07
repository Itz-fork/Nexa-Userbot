# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os

from pyrogram.types import Message
from httpx import AsyncClient
from nexa_userbot import CMD_HELP
from nexa_userbot.helpers.pyrogram_help import get_arg
from nexa_userbot.core.main_cmd import nexaub, e_or_r
from config import Config


# Help
mod_name = os.path.basename(__file__)[:-3]

CMD_HELP.update(
    {
        f"{mod_name}": f"""
**Github,**

  ✘ `github` - To Search for a github user

**Example:**

  ✘ `github`,
   ⤷ Send command with username = `{Config.CMD_PREFIX}github Itz-fork`
""",
        f"{mod_name}_category": "tools"
    }
)


# Function to get data from github API
async def get_data(username):
    base_msg = ""
    async with AsyncClient() as gpx:
        req = (await gpx.get(f"https://api.github.com/users/{username}")).json()
        # Parsing data
        try:
            avatar = req["avatar_url"]
            twitter = req['twitter_username']
            base_msg += "**❆ Gitub Information ❆** \n\n"
            base_msg += f"**Profile Url:** {req['html_url']} \n"
            base_msg += f"**Name:** `{req['name']}` \n"
            base_msg += f"**Username:** `{req['login']}` \n"
            base_msg += f"**User ID:** `{req['id']}` \n"
            base_msg += f"**Location:** `{req['location']}` \n"
            base_msg += f"**Company:** `{req['company']}` \n"
            base_msg += f"**Blog:** `{req['name']}` \n"
            base_msg += f"**Twitter:** `{f'https://twitter.com/{twitter}' if twitter else 'None'}` \n"
            base_msg += f"**Bio:** `{req['bio']}` \n"
            base_msg += f"**Public Repos:** `{req['public_repos']}` \n"
            base_msg += f"**Public Gists:** `{req['public_gists']}` \n"
            base_msg += f"**Followers:** `{req['followers']}` \n"
            base_msg += f"**Following:** `{req['following']}` \n"
            base_msg += f"**Created At:** `{req['created_at']}` \n"
            base_msg += f"**Update At:** `{req['updated_at']}` \n"
            return [base_msg, avatar]
        except Exception as e:
            base_msg += f"**An error occured while parsing the data!** \n\n**Traceback:** \n `{e}` \n\n`Make sure that you've sent the command with the correct username!`"
            return [base_msg, "https://telegra.ph//file/32f69c18190666ea96553.jpg"]


@nexaub.on_cmd(command=["github", "git"])
async def github_search(_, message: Message):
    git_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    username = get_arg(message)
    if not username:
        return await git_msg.edit("`Give a github username to get information!`")
    details = await get_data(username)
    await git_msg.reply_photo(details[1], caption=details[0])
    await git_msg.delete()