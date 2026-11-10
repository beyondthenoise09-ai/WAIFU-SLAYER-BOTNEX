import os
import time
import random
import asyncio
import subprocess
import urllib.request
from html import escape
from pyrogram import filters
from pyrogram.enums import ChatType, ChatAction, ButtonStyle, ParseMode
from pyrogram.types import InlineKeyboardMarkup, Message, InlineKeyboardButton
from youtubesearchpython.__future__ import VideosSearch

import config
from SHIVMUSIC import app
from SHIVMUSIC.misc import _boot_, SUDOERS
from SHIVMUSIC.plugins.sudo.sudoers import sudoers_list
from SHIVMUSIC.utils.database import (
    add_served_chat,
    add_served_user,
    blacklisted_chats,
    get_lang,
    is_banned_user,
    is_on_off,
)
from SHIVMUSIC.utils.decorators.language import LanguageStart
from SHIVMUSIC.utils.formatters import get_readable_time
from SHIVMUSIC.utils.inline import help_pannel, private_panel, start_panel
from SHIVMUSIC.utils.inline.help import is_owner_user
from SHIVMUSIC.utils.html_builder import build_welcome_html
from SHIVMUSIC.utils.progress import stream_typewriter_rich_message
from SHIVMUSIC.utils import start_media
from config import BANNED_USERS, START_IMG_URL, CMBOT
from strings import get_string

# ─── 2.8 MB VIDEO AUTO-DOWNLOADER, THUMBNAIL & CACHE ───
VIDEO_URL = start_media.VIDEO_URL
LOCAL_VIDEO_PATH = "/tmp/waifu_start_2mb.mp4"
LOCAL_THUMB_PATH = "/tmp/waifu_thumb.jpg"
CACHED_VIDEO_ID = None


def download_video_sync():
    if not os.path.exists(LOCAL_VIDEO_PATH) or os.path.getsize(LOCAL_VIDEO_PATH) < 10000:
        req = urllib.request.Request(
            VIDEO_URL,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
        with urllib.request.urlopen(req, timeout=30) as response, open(LOCAL_VIDEO_PATH, "wb") as out_file:
            out_file.write(response.read())

    # Generate preview thumbnail via ffmpeg so Telegram never shows a black screen
    if not os.path.exists(LOCAL_THUMB_PATH):
        try:
            subprocess.run(
                [
                    "ffmpeg", "-y", "-i", LOCAL_VIDEO_PATH,
                    "-ss", "00:00:01", "-vframes", "1",
                    "-vf", "scale=320:-1", LOCAL_THUMB_PATH,
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=10,
            )
        except Exception:
            pass

    thumb = LOCAL_THUMB_PATH if os.path.exists(LOCAL_THUMB_PATH) else None
    return LOCAL_VIDEO_PATH, thumb


def get_style_map():
    return {1: ButtonStyle.PRIMARY, 2: ButtonStyle.SUCCESS, 3: ButtonStyle.DANGER}


def create_btn(text, cb=None, url=None, user_id=None, style=ButtonStyle.PRIMARY, no_emoji=True):
    kwargs = {"text": text, "style": style}
    if cb is not None:
        kwargs["callback_data"] = cb
    if url is not None:
        kwargs["url"] = url
    if user_id is not None:
        kwargs["user_id"] = user_id
    return InlineKeyboardButton(**kwargs)


# ─── OPTIONAL: GALLERY SE DIRECT VIDEO SET KARNE KA COMMAND ───
@app.on_message(filters.video & filters.private & ~BANNED_USERS)
async def set_custom_start_video(client, message: Message):
    global CACHED_VIDEO_ID
    if message.caption and "/setvideo" in message.caption.lower():
        CACHED_VIDEO_ID = message.video.file_id
        start_media.cached_video_id = CACHED_VIDEO_ID
        await message.reply_text(
            f"✅ <b>Start Video Successfully Updated!</b>\n\n<b>Your Bot's Permanent File ID:</b>\n<code>{CACHED_VIDEO_ID}</code>",
            parse_mode=ParseMode.HTML,
        )


# ────────────────────────────────────────────────
@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    global CACHED_VIDEO_ID
    if not CACHED_VIDEO_ID:
        CACHED_VIDEO_ID = start_media.cached_video_id
    await add_served_user(message.from_user.id)

    # ─── 1. BOTNEX TYPOGRAPHY INTRO ───
    try:
        intro = await message.reply_text("✨ <b>ʜᴇʏ ʙᴀʙʏ...😘</b>")
        await asyncio.sleep(0.4)
        await intro.edit_text("✨ <b>ʜᴇʏ ʙᴀʙʏ, ᴡᴀɪᴛ ᴀ sᴇᴄᴏɴᴅ... 🎧</b>")
        await asyncio.sleep(0.5)
        await intro.edit_text("⚡ <b>ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ʙᴏᴛɴᴇx ɴᴇᴛᴡᴏʀᴋ...</b>")
        await asyncio.sleep(0.4)
        box_text = (
            "┏━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
            "   🎧 <b>ᴡ ᴀ ɪ ғ ᴜ  •  s ʟ ᴀ ʏ ᴇ ʀ</b>\n"
            "   ⚡ <i>ᴘᴏᴡᴇʀᴇᴅ ʙʏ ʙᴏᴛɴᴇx ᴄᴏʀᴇ</i>\n"
            "┗━━━━━━━━━━━━━━━━━━━━━━━━┛\n"
            "✨ <b>ʟᴏᴀᴅɪɴɢ ʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴇxᴘᴇʀɪᴇɴᴄᴇ...😘</b>"
        )
        await intro.edit_text(box_text)
        await asyncio.sleep(0.7)
        await intro.delete()
    except Exception:
        pass

    # ─── 2. PERMANENT CUTE STICKER (No Delete) ───
    try:
        await message.reply_sticker("CAACAgUAAxkBAAEwa5xq8XGxjm9OyhtA5gXr-kzK9le5OgACjCcAAkfkaFd22VAOl17duD0E")
    except Exception:
        pass

    # ─── 3. WELCOME MESSAGE ISKE THEEK NICHE AAYEGA ───
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        if name[0:4] == "help":
            keyboard = help_pannel(_, False, is_owner_user(message.from_user.id))
            await app.send_chat_action(message.chat.id, ChatAction.TYPING)
            return await message.reply_photo(
                random.choice(START_IMG_URL),
                caption=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=keyboard,
            )
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            if await is_on_off(2):
                return await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"✨ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>sᴜᴅᴏʟɪsᴛ</b>.\n\n👤 <b>ᴜsᴇʀ ɪᴅ ➠</b> <code>{message.from_user.id}</code>\n📍 <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.from_user.username}",
                )
            return
        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"

            try:
                results = VideosSearch(query, limit=1)
                search_data = await results.next()

                if not search_data or not search_data.get("result"):
                    return await m.edit_text("❌ Track details not found. The video might be restricted or deleted.")

                result = search_data["result"][0]
                title = result.get("title", "Unknown Title")
                duration = result.get("duration", "Unknown Duration")
                views = result.get("viewCount", {}).get("short", "0")

                thumbnails = result.get("thumbnails", [])
                thumbnail = thumbnails[0]["url"].split("?")[0] if thumbnails else random.choice(START_IMG_URL)

                channellink = result.get("channel", {}).get("link", "")
                channel = result.get("channel", {}).get("name", "Unknown Channel")
                link = result.get("link", query)
                published = result.get("publishedTime", "Unknown Date")

                searched_text = _["start_6"].format(
                    title, duration, views, published, channellink, channel, app.mention
                )

                s_map = get_style_map()
                key = InlineKeyboardMarkup(
                    [
                        [
                            create_btn(text=_["S_B_8"], url=link, style=s_map[2]),
                            create_btn(text=_["S_B_9"], url=config.SUPPORT_CHAT, style=s_map[2]),
                        ],
                    ]
                )
                await m.delete()
                await app.send_photo(
                    chat_id=message.chat.id,
                    photo=thumbnail,
                    caption=searched_text,
                    reply_markup=key,
                )
                if await is_on_off(2):
                    return await app.send_message(
                        chat_id=config.LOGGER_ID,
                        text=f"✨ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ ᴛᴏ ᴄʜᴇᴄᴋ <b>ᴛʀᴀᴄᴋ ɪɴғᴏʀᴍᴀᴛɪᴏɴ</b>.\n\n👤 <b>ᴜsᴇʀ ɪᴅ ➠</b> <code>{message.from_user.id}</code>\n📍 <b>ᴜsᴇʀɴᴀᴍᴇ ➠</b> @{message.from_user.username}",
                    )
                return
            except Exception as e:
                return await m.edit_text(
                    f"❌ <b>Track information unavailable</b>\n\n<code>{escape(str(e))}</code>",
                    parse_mode=ParseMode.HTML,
                )
    else:
        out = private_panel(_)
        await app.send_chat_action(message.chat.id, ChatAction.UPLOAD_VIDEO)

        clean_caption = build_welcome_html(
            message.from_user.mention, app.mention, app.username
        )

        try:
            if CACHED_VIDEO_ID:
                await message.reply_video(
                    video=CACHED_VIDEO_ID,
                    caption=clean_caption,
                    reply_markup=InlineKeyboardMarkup(out),
                    parse_mode=ParseMode.HTML,
                    supports_streaming=True,
                )
            else:
                try:
                    # 2.8 MB file Telegram direct URL se fetch karke native preview & timer banata hai
                    sent_vid = await message.reply_video(
                        video=VIDEO_URL,
                        caption=clean_caption,
                        reply_markup=InlineKeyboardMarkup(out),
                        parse_mode=ParseMode.HTML,
                        supports_streaming=True,
                    )
                except Exception:
                    # Fallback: local download + ffmpeg thumbnail + streaming metadata
                    video_path, thumb_path = await asyncio.to_thread(download_video_sync)
                    sent_vid = await message.reply_video(
                        video=video_path,
                        thumb=thumb_path,
                        duration=14,
                        width=720,
                        height=1280,
                        caption=clean_caption,
                        reply_markup=InlineKeyboardMarkup(out),
                        parse_mode=ParseMode.HTML,
                        supports_streaming=True,
                    )
                if sent_vid and sent_vid.video:
                    CACHED_VIDEO_ID = sent_vid.video.file_id
                    start_media.cached_video_id = CACHED_VIDEO_ID
        except Exception as e:
            print(f"Video Error: {e}")
            await message.reply_text(
                text=clean_caption,
                reply_markup=InlineKeyboardMarkup(out),
                parse_mode=ParseMode.HTML,
            )

        if await is_on_off(2):
            try:
                await app.send_message(
                    chat_id=config.LOGGER_ID,
                    text=f"✨ {message.from_user.mention} ᴊᴜsᴛ sᴛᴀʀᴛᴇᴅ ᴛʜᴇ ʙᴏᴛ.\n\n<b>⭐ ᴜsᴇʀ ɪᴅ :</b> <code>{message.from_user.id}</code>",
                )
            except Exception:
                pass


@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    await message.reply_text(
        text=build_welcome_html(
            message.from_user.mention, app.mention, app.username
        ),
        reply_markup=InlineKeyboardMarkup(out),
        parse_mode=ParseMode.HTML,
    )
    return await add_served_chat(message.chat.id)


@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except Exception:
                    pass
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(
                        _["start_5"].format(
                            app.mention,
                            f"https://t.me/{app.username}?start=sudolist",
                            config.SUPPORT_CHAT,
                        ),
                        disable_web_page_preview=True,
                    )
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                await message.reply_text(
                    text=build_welcome_html(
                        message.from_user.mention, app.mention, app.username
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                    parse_mode=ParseMode.HTML,
                )
                await add_served_chat(message.chat.id)
                await message.stop_propagation()
        except Exception as ex:
            print(ex)
