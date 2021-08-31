# Copyright (c) 2021 Itz-fork
# Part of: Nexa-Userbot

import os
import re
from aiohttp import ClientSession
from Python_ARQ import ARQ
from pyrogram.types import Message

from nexa_userbot import CMD_HELP
from nexa_userbot.core.main_cmd import nexaub_on_cmd, e_or_r
from nexa_userbot.core.nexaub_database.nexaub_db_conf import set_arq_key, get_arq_key
from nexa_userbot.helpers.pyrogram_help import get_arg
from config import Config


# Help
CMD_HELP.update(
    {
        "arq": f"""
**ARQ,**

  ✘ `lyrics` - To Get Lyrics for Given Keyword
  ✘ `tr` - To Translate a word / sentence
  ✘ `wiki` - To Search Wiki
  ✘ `reddit` - To Search Reddit

**Example:**

  ✘ `lyrics`,
   ⤷ Send with keyword = `{Config.CMD_PREFIX}lyrics your_song_name`
   ⤷ Reply to a text message with `{Config.CMD_PREFIX}lyrics`

  ✘ `tr`,
   ⤷ Send with keyword = `{Config.CMD_PREFIX}tr hola!en` (Replace en with your dest. lang code)
   ⤷ Reply to a text message with `{Config.CMD_PREFIX}tr en` (Replace en with your dest. lang code)

  ✘ `wiki`,
   ⤷ Send with keyword = `{Config.CMD_PREFIX}wiki google`
   ⤷ Reply to a text message with `{Config.CMD_PREFIX}wiki`

  ✘ `reddit`,
   ⤷ Send with keyword = `{Config.CMD_PREFIX}reddit doge`
   ⤷ Reply to a text message with `{Config.CMD_PREFIX}reddit`
"""
    }
)

mod_file = os.path.basename(__file__)


# Do stuff with arq

# Closing aiohttp session
async def close_session(aiohtp_c):
    await aiohtp_c.close()

async def ARQ_NEXAUB(
    keyword,
    dest_lang="en",
    is_lyrics=False,
    is_tr=False,
    is_wiki=False,
    is_reddit=False):
    try:
        # ARQ Client
        arq_aiohttp = ClientSession()
        arq_url = "https://thearq.tech/"
        arq_api = await get_arq_key()
        if arq_api is None:
            return print("ARQ_API_KEY isn't in database. Add it and Try Again!")
        arq_nexaub = ARQ(arq_url, arq_api, arq_aiohttp)
        # === Now do stuff with arq === #
        # lyrics module
        if is_lyrics:
            lyric = await arq_nexaub.lyrics(query=keyword)
            await close_session(arq_aiohttp)
            return lyric
        # Translator module
        if is_tr:
            transed = await arq_nexaub.translate(text=keyword, destLangCode=dest_lang)
            await close_session(arq_aiohttp)
            return transed.result
        # Wiki module
        if is_wiki:
            wiki_s = await arq_nexaub.wiki(query=keyword)
            await close_session(arq_aiohttp)
            return wiki_s.result
        # Reddit Module
        if is_reddit:
            reddit_s = await arq_nexaub.reddit(query=keyword)
            await close_session(arq_aiohttp)
            return reddit_s
    except Exception as e:
        print(e)

# Lyrics
@nexaub_on_cmd(command="lyrics", modlue=mod_file)
async def arq_lyrics(_, message: Message):
    lyrics_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    keyword = get_arg(message)
    r_keyword = message.reply_to_message
    if not keyword:
        if r_keyword:
            keyword = r_keyword.text
        else:
            return await lyrics_msg.edit("`Give a song name to get lyrics!`")
    else:
        keyword = keyword
    f_lyrics = await ARQ_NEXAUB(keyword=keyword, is_lyrics=True)
    nyc_lyrics = f_lyrics.result
    if len(nyc_lyrics) > 4096:
        await lyrics_msg.edit("`Wah!! Long Lyrics tho!, Wait I'm sending it as a file!`")
        lyric_file = open("lyrics_NEXAUB.txt", "w+")
        lyric_file.write(nyc_lyrics)
        lyric_file.close()
        await lyrics_msg.reply_document("lyrics_NEXAUB.txt")
        os.remove("lyrics_NEXAUB.txt")
        await lyrics_msg.delete()
    else:
        await lyrics_msg.edit(nyc_lyrics)

# Translator
@nexaub_on_cmd(command="tr", modlue=mod_file)
async def arq_trans(_, message: Message):
    trans_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    to_tr_text = get_arg(message)
    r_tr_text = message.reply_to_message
    if r_tr_text:
        trans_this = r_tr_text.text
        if not to_tr_text:
            dest_l = "en"
        else:
            dest_l = to_tr_text
    else:
        try:
            string_c = to_tr_text.replace(".tr ", "").split("!")
            trans_this = string_c[0]
            dest_l = string_c[1]
        except:
            return await trans_msg.edit(f"`Error Occured While Splitting Text! Please Read Examples in Help Page!` \n\n**Help:** `{Config.CMD_PREFIX}help arq`")
    translate_txt = await ARQ_NEXAUB(is_tr=True, keyword=trans_this, dest_lang=dest_l)
    translated_str = f"""
**Translated,**

**From:** `{translate_txt.src}`
**To:** `{translate_txt.dest}`
**Translation:**
`{translate_txt.translatedText}`
"""
    if len(translated_str) > 4096:
        await trans_msg.edit("`Wah!! Translated Text So Long Tho!, Give me a minute, I'm sending it as a file!`")
        tr_txt_file = open("translated_NEXAUB.txt", "w+")
        tr_txt_file.write(translated_str)
        tr_txt_file.close()
        await trans_msg.reply_document("translated_NEXAUB.txt")
        os.remove("translated_NEXAUB.txt")
        await trans_msg.delete()
    else:
        await trans_msg.edit(translated_str)

# Wiki search
@nexaub_on_cmd(command="wiki", modlue=mod_file)
async def arq_wiki(_, message: Message):
    wiki_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    wiki_key = get_arg(message)
    r_wiki_key = message.reply_to_message
    if not wiki_key:
        if r_wiki_key:
            wiki_this = r_wiki_key.text
        else:
            return await wiki_msg.edit("`Give something to search!`")
    else:
        wiki_this = wiki_key
    s_wiki = await ARQ_NEXAUB(is_wiki=True, keyword=wiki_this)
    wiki_txt = f"""
**Title:** `{s_wiki.title}`
**Answer:**
`{s_wiki.answer}`
"""
    if len(wiki_txt) > 4096:
        await wiki_msg.edit("`Big stuff to read!! Lemme send it as a text file :)`")
        wiki_txt_file = open("wiki_NEXAUB.txt", "w+")
        wiki_txt_file.write(wiki_txt)
        wiki_txt_file.close()
        await wiki_msg.reply_document("wiki_NEXAUB.txt")
        os.remove("wiki_NEXAUB.txt")
        await wiki_msg.delete()
    else:
        await wiki_msg.edit(wiki_txt)

# Reddit
@nexaub_on_cmd(command="reddit", modlue=mod_file)
async def arq_reddit(_, message: Message):
    red_msg = await e_or_r(nexaub_message=message, msg_text="`Processing...`")
    reddit_key = get_arg(message)
    r_reddit_msg = message.reply_to_message
    if not reddit_key:
        if r_reddit_msg:
            reddit_this = r_reddit_msg.text
        else:
            return await red_msg.edit("`Give some text to quote!`")
    else:
        reddit_this = reddit_key
    reddit_now = await ARQ_NEXAUB(is_reddit=True, keyword=reddit_this)
    try:
        _reddit = reddit_now.result
        r_post = _reddit.postLink
        r_subreddit = _reddit.subreddit
        r_title = _reddit.title
        r_image = _reddit.url
        r_user = _reddit.author
        r_txt = f"""
**Title:** `{r_title}`
**Subreddit:** `{r_subreddit}`
**Author:** `{r_user}`
**Post Link:** `{r_post}`
"""
        await red_msg.reply_photo(photo=r_image, caption=r_txt)
        await red_msg.delete()
    except Exception as e:
        await red_msg.edit("`Ooops!, Something went wrong; Check your keyword!`")
