# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Friday Userbot | DevsExpo | Itz-fork

import os
import sys
import git

from pyrogram import filters
from pyrogram.types import Message
from os import environ, execle

from config import Config
from pyrogram_ub.helpers.pyrogram_help import get_arg, run_shell_cmds
from pyrogram_ub import NEXAUB, CMD_HELP

REPO_ = Config.UPSTREAM_REPO
BRANCH_ = Config.U_BRANCH


@NEXAUB.on_message(filters.me & filters.command("update", Config.CMD_PREFIX))
async def update_it(_, message: Message):
    update_msg = await message.edit("`Processing...`")
    try:
         nexa_ub_repo = git.Repo()
    except git.GitCommandError:
        return await update_msg.edit("`Invalid Git Command`!")
    except git.InvalidGitRepositoryError:
        nexa_ub_repo = git.Repo.init()
    try:
        up_txt = message.text
        if "now" in up_txt:
            if "upstream" in nexa_ub_repo.remotes:
                origin = nexa_ub_repo.remote("upstream")
            else:
                origin = nexa_ub_repo.create_remote("upstream", REPO_)
            origin.fetch()
            nexa_ub_repo.create_head(Config.U_BRANCH, origin.refs.master)
            nexa_ub_repo.heads.master.set_tracking_branch(origin.refs.master)
            nexa_ub_repo.heads.master.checkout(True)
        if nexa_ub_repo.active_branch.name != Config.U_BRANCH:
            return await update_msg.edit(f"`Can't update your Nexa-Userbot becuase you're using a custom branch.` \n\n**Default Branch:** `{nexa_ub_repo.active_branch.name}` \n**Active Branch:** `{Config.U_BRANCH}`")
        try:
            nexa_ub_repo.create_remote("upstream", REPO_)
        except BaseException:
            pass
        ups_rem = nexa_ub_repo.remote("upstream")
        ups_rem.fetch(Config.U_BRANCH)
        if not Config.HEROKU_URL:
            try:
                ups_rem.pull(Config.U_BRANCH)
            except git.GitCommandError:
                nexa_ub_repo.git.reset("--hard", "FETCH_HEAD")
            await run_shell_cmds("pip3 install --no-cache-dir -r requirements.txt")
            await update_msg("`Successfully Updated! Restarting Now...`")
            p = os.getcwd()
            path = f"{p}/Nexa-Userbot/startup.sh"
            cmd = f"bash {path}"
            run_shell_cmds(cmd)
            exit()
            return
        else:
            await update_msg.edit("`Heroku Detected...`")
            ups_rem.fetch(Config.U_BRANCH)
            nexa_ub_repo.git.reset("--hard", "FETCH_HEAD")
            if "heroku" in nexa_ub_repo.remotes:
                remote = nexa_ub_repo.remote("heroku")
                remote.set_url(Config.HEROKU_URL)
            else:
                remote = nexa_ub_repo.create_remote("heroku", Config.HEROKU_URL)
            try:
                remote.push(refspec="HEAD:refs/heads/master", force=True)
            except BaseException as e:
                await update_msg.edit(f"**Error:** {e}")
                return nexa_ub_repo.__del__()
    except Exception as e:
        await update_msg.edit(f"**Error:** `{e}`")
