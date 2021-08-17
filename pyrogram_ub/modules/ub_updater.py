# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot
# Credits: Developers Userbot | okay-retard | Zect Userbot

import heroku3
import asyncio
import sys

from os import environ, execle, path, remove
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError
from pyrogram import filters

from pyrogram_ub import NEXAUB, CMD_HELP
from config import Config
from pyrogram_ub.helpers.pyrogram_help import get_arg


CMD_HELP.update(
    {
        "updater": """
**Updater**

  ✘ `update` - To Updater Your Userbot
  ✘ `restart` - To Restart Your Userbot (Heroku Only)
  ✘ `logs` - To Get Logs of Your Userbot (Heroku Only)
"""
    }
)

UPSTREAM_REPO_URL = "https://github.com/Itz-fork/Nexa-Userbot"
requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "On %d/%m/%y at %H:%M:%S"
    for c in repo.iter_commits(diff):
        ch_log += f"**#{c.count()}** : {c.committed_datetime.strftime(d_form)} : [{c.summary}]({UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}) by `{c.author}`\n"
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@NEXAUB.on_message(filters.command("update", Config.CMD_PREFIX) & filters.me)
async def upstream(client, message):
    status = await message.edit(f"`Checking For Updates from` [Nexa-Userbot]({UPSTREAM_REPO_URL}) `Repo...`")
    conf = get_arg(message)
    off_repo = UPSTREAM_REPO_URL
    try:
        txt = "`Oops! Updater Can't Continue...`"
        txt += "**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await status.edit(f"{txt}\n`directory {error} is not found`")
        repo.__del__()
        return
    except GitCommandError as error:
        await status.edit(f"{txt}\n`Early failure! {error}`")
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            pass
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != "master":
        await status.edit(
            f"`Can't update your Nexa-Userbot becuase you're using a custom branch.` \n\n**Default Branch:** `master` \n**You are on:** `{ac_br}` \n`Please change to master branch.`"
        )
        repo.__del__()
        return
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if "now" not in conf:
        if changelog:
            changelog_str = f"**New Update available** \n\n**Branch:** [[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br}) \n\n**Changelog:** \n\n{changelog}"
            if len(changelog_str) > 4096:
                await status.edit("`Changelog is too big, view the file to see it.`")
                file = open("output.txt", "w+")
                file.write(changelog_str)
                file.close()
                await NEXAUB.send_document(
                    message.chat.id,
                    "output.txt",
                    caption=f"Do `{Config.CMD_PREFIX}update now` to update your Nexa-Userbot",
                    reply_to_message_id=status.message_id,
                )
                remove("output.txt")
            else:
                return await status.edit(
                    f"{changelog_str}\n\nDo `.update now` to update your Nexa-Userbot",
                    disable_web_page_preview=True,
                )
        else:
            await status.edit(
                f"\n**Nexa-Userbot is Uptodate with** [[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br})**\n",
                disable_web_page_preview=True,
            )
            repo.__del__()
            return
    if Config.HEROKU_API_KEY is not None:
        heroku = heroku3.from_key(Config.HEROKU_API_KEY)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not Config.HEROKU_APP_NAME:
            await status.edit(
                "**Error:** `Please add HEROKU_APP_NAME variable to continue update!`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == Config.HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await status.edit(
                f"{txt}\n`Invalid Heroku credentials.`"
            )
            repo.__del__()
            return
        await status.edit(
            "`Userbot Dyno Build is in Progress! Please wait...`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + Config.HEROKU_API_KEY + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError as error:
            pass
        await status.edit("`Successfully Updated!` \n`Restarting Now...`")
    else:
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await status.edit("`Successfully Updated!` \nRestarting Now...`",)
        args = [sys.executable, "./startup.sh"]
        execle(sys.executable, *args, environ)
        return

@NEXAUB.on_message(filters.command("restart", Config.CMD_PREFIX) & filters.me)
async def restart(client, message):
    try:
        await message.edit("`Nexa-Userbot is restarting! Please wait...`")
        heroku_conn = heroku3.from_key(Config.HEROKU_API_KEY)
        server = heroku_conn.app(Config.HEROKU_APP_NAME)
        server.restart()
    except Exception as e:
        await message.edit(f"Vaiable(s) `HEROKU_APP_NAME` or `HEROKU_API_KEY` is **Wrong** or **Not Filled**! \n`Please fill or correct them!` \n\n**Error:** `{e}`")


@NEXAUB.on_message(filters.command("logs", Config.CMD_PREFIX) & filters.me)
async def log(client, message):
    try:
        await message.edit("`Getting Logs`")
        heroku_conn = heroku3.from_key(Config.HEROKU_API_KEY)
        server = heroku_conn.get_app_log(Config.HEROKU_APP_NAME, dyno='worker', lines=100, source='app', timeout=100)
        f_logs = server
        if len(f_logs) > 4096:
            file = open("logs.txt", "w+")
            file.write(f_logs)
            file.close()
            await NEXAUB.send_document(message.chat.id, "logs.txt", caption=f"Logs of `{Config.HEROKU_APP_NAME}`")
            remove("logs.txt")
    except Exception as e:
        await message.edit(f"**Error:** `{e}`")
