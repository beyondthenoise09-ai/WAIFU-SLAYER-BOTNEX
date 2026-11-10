import asyncio
import random
import math
from pyrogram.types import CallbackQuery, InputMediaPhoto, InputMediaVideo, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from pyrogram.errors import WebpageMediaEmpty, MessageNotModified
from pyrogram.enums import ButtonStyle, ChatMemberStatus, ParseMode

from SHIVMUSIC import YouTube, app
from SHIVMUSIC.core.call import ANJALI
from SHIVMUSIC.misc import SUDOERS, db
from SHIVMUSIC.utils.database import (
    get_active_chats, get_lang, get_upvote_count, is_active_chat,
    is_music_playing, is_nonadmin_chat, music_off, music_on, set_loop, get_assistant,
    is_autoplay_on, autoplay_on, autoplay_off
)

from SHIVMUSIC.utils.decorators.language import languageCB
from SHIVMUSIC.utils.formatters import seconds_to_min
from SHIVMUSIC.utils.inline import close_markup, stream_markup, stream_markup_timer
from SHIVMUSIC.utils.stream.autoclear import auto_clean
from SHIVMUSIC.utils.thumbnails import get_thumb
import config
from config import (
    BANNED_USERS, SOUNCLOUD_IMG_URL, STREAM_IMG_URL, TELEGRAM_AUDIO_URL,
    TELEGRAM_VIDEO_URL, START_IMG_URL, adminlist, confirmer, votemode
)
from strings import get_string
from SHIVMUSIC.utils.inline.start import private_panel
from SHIVMUSIC.utils.html_builder import build_welcome_html
from SHIVMUSIC.utils import start_media

checker = {}
upvoters = {}

def get_style_map():
    return {1: ButtonStyle.PRIMARY, 2: ButtonStyle.SUCCESS, 3: ButtonStyle.DANGER, 4: ButtonStyle.PRIMARY}


def create_btn(text, cb=None, url=None, style=ButtonStyle.PRIMARY, emoji_id=None, no_emoji=True):
    kwargs = {"text": text, "style": style}
    if cb is not None:
        kwargs["callback_data"] = cb
    if url is not None:
        kwargs["url"] = url
    return InlineKeyboardButton(**kwargs)

@app.on_callback_query(filters.regex("settingsback_helper") & ~BANNED_USERS)
@languageCB
async def settings_back_helper(client, CallbackQuery, _):
    try:
        await CallbackQuery.answer()
    except:
        pass

    caption = build_welcome_html(
        CallbackQuery.from_user.mention, app.mention, app.username
    )
    markup = InlineKeyboardMarkup(private_panel(_))

    async def _restore_video(video):
        edited = await CallbackQuery.edit_message_media(
            media=InputMediaVideo(
                media=video,
                caption=caption,
                parse_mode=ParseMode.HTML,
                supports_streaming=True,
            ),
            reply_markup=markup,
        )
        try:
            if edited and edited.video and not start_media.cached_video_id:
                start_media.cached_video_id = edited.video.file_id
        except Exception:
            pass

    # 0) Message is already the start video -> only swap caption + buttons.
    #    No media re-upload, so no flood and no Neon image.
    try:
        _m = CallbackQuery.message
        if _m and (_m.video or _m.animation):
            await CallbackQuery.edit_message_caption(
                caption, parse_mode=ParseMode.HTML, reply_markup=markup
            )
            return
    except MessageNotModified:
        return
    except Exception:
        pass

    # 1) Restore the same start VIDEO (this was the Neon-image bug: the old code
    #    replaced the video with START_IMG_URL photo on every Back press).
    candidates = []
    if start_media.cached_video_id:
        candidates.append(start_media.cached_video_id)
    candidates.append(start_media.VIDEO_URL)
    for video in candidates:
        try:
            await _restore_video(video)
            return
        except MessageNotModified:
            return
        except Exception:
            continue

    # 2) Fallback: photo (only if the video could not be loaded at all)
    try:
        if isinstance(START_IMG_URL, list):
            img = random.choice(START_IMG_URL)
        else:
            img = START_IMG_URL
        await CallbackQuery.edit_message_media(
            media=InputMediaPhoto(media=img, caption=caption, parse_mode=ParseMode.HTML),
            reply_markup=markup,
        )
        return
    except MessageNotModified:
        return
    except Exception:
        pass

    # 3) Last resort: plain text message (e.g. panel opened in a text message)
    try:
        await CallbackQuery.edit_message_text(
            caption, reply_markup=markup, parse_mode=ParseMode.HTML
        )
    except Exception:
        pass

@app.on_callback_query(filters.regex("support_page") & ~BANNED_USERS)
@languageCB
async def support_page_cb(client, CallbackQuery, _):
    await CallbackQuery.answer()
    support_text = (
        "<b>◈ BOTNEX · SUPPORT DESK</b>\n"
        "<i>WAIFU-SLAYER · PROJECT 001</i>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        "Need help with setup, playback or a feature? "
        "Reach the support community or follow the updates channel below.\n\n"
        "<code>WE BUILD. YOU PLAY.</code>"
    )
    buttons = []
    links = []
    links.append(create_btn("💬 ᴊᴏɪɴ sᴜᴘᴘᴏʀᴛ", url=config.SUPPORT_CHAT or config.BOTNEX_GROUP_LINK, style=ButtonStyle.SUCCESS))
    links.append(create_btn("🚀 ᴜᴘᴅᴀᴛᴇs ↗", url=config.SUPPORT_CHANNEL or config.BOTNEX_GROUP_LINK, style=ButtonStyle.SUCCESS))
    if links:
        buttons.append(links)
    buttons.append([create_btn("‹ BACK", cb="settingsback_helper", style=ButtonStyle.PRIMARY)])
    return await CallbackQuery.edit_message_caption(
        caption=support_text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(buttons),
    )


@app.on_callback_query(filters.regex("gib_source") & ~BANNED_USERS)
async def gib_repo_callback(_, callback_query):
    try:
        caption = (
            "✨ <b>ʙᴏᴛɴᴇx</b> ⋆ ࣪ 𝜗𝜚  <code>ᴘʀᴏᴊᴇᴄᴛ 001</code>\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n\n"
            "🎀 <b>ᴡᴀɪғᴜ ✗ sʟᴀʏᴇʀ</b> 🎧\n"
            "<i>ᴀ ᴘʀᴇᴍɪᴜᴍ ᴛᴇʟᴇɢʀᴀᴍ ᴠᴏɪᴄᴇ-ᴄʜᴀᴛ ᴍᴜsɪᴄ sʏsᴛᴇᴍ ғᴏʀ ɢʀᴏᴜᴘs.</i>\n\n"
            "🎵 ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴍᴜsɪᴄ sᴛʀᴇᴀᴍɪɴɢ\n"
            "📑 sᴍᴀʀᴛ ǫᴜᴇᴜᴇ ᴍᴀɴᴀɢᴇᴍᴇɴᴛ\n"
            "🔁 ʀᴇʟᴀᴛᴇᴅ-ᴛʀᴀᴄᴋ ᴀᴜᴛᴏᴘʟᴀʏ\n"
            "🎚️ ᴇǫᴜᴀʟɪᴢᴇʀ & ᴘʟᴀʏʙᴀᴄᴋ ᴄᴏɴᴛʀᴏʟs\n\n"
            "💎 <b>ᴅᴇᴠᴇʟᴏᴘᴇᴅ & ᴄᴜsᴛᴏᴍɪᴢᴇᴅ ʙʏ ᴄʜᴀɴᴅᴀɴ</b>\n"
            "💬 ᴊᴏɪɴ ᴏᴜʀ ᴄᴏᴍᴍᴜɴɪᴛʏ ʙᴇʟᴏᴡ ⬇️\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        )
        buttons = [
            [
                create_btn("💬 ᴏᴜʀ ɢʀᴏᴜᴘ", url=config.BOTNEX_GROUP_LINK, style=ButtonStyle.SUCCESS),
                create_btn("👑 ᴏᴡɴᴇʀ", url=config.BOTNEX_OWNER_LINK, style=ButtonStyle.SUCCESS),
            ]
        ]
        if config.GITHUB and config.GITHUB.startswith("https://"):
            buttons.append([create_btn("⌘ PROJECT SOURCE", url=config.GITHUB, style=ButtonStyle.PRIMARY)])
        buttons.append([create_btn("‹ BACK", cb="settingsback_helper", style=ButtonStyle.PRIMARY), create_btn("✕ CLOSE", cb="close", style=ButtonStyle.DANGER)])
        await callback_query.edit_message_caption(
            caption=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except MessageNotModified:
        pass
    except Exception as e:
        await callback_query.answer(f"Unable to open this panel: {str(e)}", show_alert=True)


@app.on_callback_query(filters.regex("botnex_info") & ~BANNED_USERS)
async def botnex_info_callback(_, callback_query):
    try:
        await callback_query.answer()
    except Exception:
        pass
    try:
        caption = (
            "💎 <b>ʙᴏᴛɴᴇx · ɪɴғᴏ</b> 🏛\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰\n\n"
            "🎧 <b>ʜᴏᴡ ᴛᴏ ᴜsᴇ</b>\n"
            "❖ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀs ᴀᴅᴍɪɴ\n"
            "❖ sᴛᴀʀᴛ ᴀ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ\n"
            "❖ ᴛʏᴘᴇ <code>/play song name</code>\n\n"
            "⚡ <b>ғᴇᴀᴛᴜʀᴇs</b>\n"
            "❖ 24x7 ᴀᴄᴛɪᴠᴇ · ʟᴀɢ-ғʀᴇᴇ ʜᴅ ᴀᴜᴅɪᴏ\n"
            "❖ ᴀᴜᴛᴏᴘʟᴀʏ · ʟᴏᴏᴘ · sʜᴜғғʟᴇ · sᴇᴇᴋ · sᴘᴇᴇᴅ\n"
            "❖ ᴍᴜʟᴛɪ-ʟᴀɴɢᴜᴀɢᴇ sᴜᴘᴘᴏʀᴛ\n\n"
            "❓ ᴛᴀᴘ <b>ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs</b> ғᴏʀ ᴛʜᴇ ғᴜʟʟ ʟɪsᴛ\n"
            "▰▰▰▰▰▰▰▰▰▰▰▰▰▰"
        )
        buttons = [
            [
                create_btn("💬 ɢʀᴏᴜᴘ", url=config.BOTNEX_GROUP_LINK, style=ButtonStyle.SUCCESS),
                create_btn("👑 ᴏᴡɴᴇʀ", url=config.BOTNEX_OWNER_LINK, style=ButtonStyle.SUCCESS),
            ],
            [
                create_btn("‹ BACK", cb="settingsback_helper", style=ButtonStyle.PRIMARY),
                create_btn("✕ CLOSE", cb="close", style=ButtonStyle.DANGER),
            ],
        ]
        await callback_query.edit_message_caption(
            caption=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(buttons),
        )
    except MessageNotModified:
        pass
    except Exception as e:
        await callback_query.answer(f"Unable to open this panel: {str(e)}", show_alert=True)

@app.on_callback_query(filters.regex("unban_assistant"))
async def unban_assistant(_, callback: CallbackQuery):
    chat_id = callback.message.chat.id
    userbot = await get_assistant(chat_id)
    try:
        await app.unban_chat_member(chat_id, userbot.id)
        await callback.answer("✅ ᴧssɪsᴛᴧηᴛ υηʙᴧηηєᴅ sυᴄᴄєssғυʟʟʏ!", show_alert=True)
    except Exception:
        await callback.answer("❌ ғᴧɪʟєᴅ ᴛσ υηʙᴧη. ɢɪᴠє ϻє ᴧᴅϻɪη ᴘєʀϻɪssɪσηs.", show_alert=True)

@app.on_callback_query(filters.regex("ADMIN") & ~BANNED_USERS)
@languageCB
async def del_back_playlist(client, CallbackQuery, _):
    callback_data = CallbackQuery.data.strip()
    callback_request = callback_data.split(None, 1)[1]
    command, chat = callback_request.split("|")
    if "_" in str(chat):
        bet = chat.split("_")
        chat = bet[0]
        counter = bet[1]
    chat_id = int(chat)
    if not await is_active_chat(chat_id):
        return await CallbackQuery.answer(_["general_5"], show_alert=True)
    mention = CallbackQuery.from_user.mention
    style_map = get_style_map()

    if command == "UpVote":
        if chat_id not in votemode: votemode[chat_id] = {}
        if chat_id not in upvoters: upvoters[chat_id] = {}

        voters = (upvoters[chat_id]).get(CallbackQuery.message.id)
        if not voters: upvoters[chat_id][CallbackQuery.message.id] = []

        vote = (votemode[chat_id]).get(CallbackQuery.message.id)
        if not vote: votemode[chat_id][CallbackQuery.message.id] = 0

        if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
            (upvoters[chat_id][CallbackQuery.message.id]).remove(CallbackQuery.from_user.id)
            votemode[chat_id][CallbackQuery.message.id] -= 1
        else:
            (upvoters[chat_id][CallbackQuery.message.id]).append(CallbackQuery.from_user.id)
            votemode[chat_id][CallbackQuery.message.id] += 1

        upvote = await get_upvote_count(chat_id)
        get_upvotes = int(votemode[chat_id][CallbackQuery.message.id])

        if get_upvotes >= upvote:
            votemode[chat_id][CallbackQuery.message.id] = upvote
            try:
                exists = confirmer[chat_id][CallbackQuery.message.id]
                current = db[chat_id][0]
                if current["vidid"] != exists["vidid"] or current["file"] != exists["file"]:
                    return await CallbackQuery.edit_message_text(_["admin_35"])
            except:
                return await CallbackQuery.edit_message_text(_["admin_36"])
            try:
                await CallbackQuery.edit_message_text(_["admin_37"].format(upvote))
            except:
                pass
            command = counter
            mention = "υᴘᴠσᴛєs"
        else:
            if CallbackQuery.from_user.id in upvoters[chat_id][CallbackQuery.message.id]:
                await CallbackQuery.answer(_["admin_38"], show_alert=True)
            else:
                await CallbackQuery.answer(_["admin_39"], show_alert=True)

            upl = InlineKeyboardMarkup([
                [create_btn(text=f"{get_upvotes}", cb=f"ADMIN  UpVote|{chat_id}_{counter}", style=style_map[1], emoji_id=6041720006973067267)]
            ])
            await CallbackQuery.answer(_["admin_40"], show_alert=True)
            return await CallbackQuery.edit_message_reply_markup(reply_markup=upl)
    else:
        is_non_admin = await is_nonadmin_chat(CallbackQuery.message.chat.id)
        if not is_non_admin:
            if CallbackQuery.from_user.id not in SUDOERS:
                admins = adminlist.get(CallbackQuery.message.chat.id)
                allowed = bool(admins and CallbackQuery.from_user.id in admins)
                if not allowed:
                    try:
                        member = await client.get_chat_member(
                            CallbackQuery.message.chat.id,
                            CallbackQuery.from_user.id,
                        )
                        allowed = member.status in (
                            ChatMemberStatus.ADMINISTRATOR,
                            ChatMemberStatus.OWNER,
                        )
                    except Exception:
                        allowed = False
                if not allowed:
                    return await CallbackQuery.answer(_["admin_14"], show_alert=True)

    if command == "Pause":
        if not await is_music_playing(chat_id): return await CallbackQuery.answer(_["admin_1"], show_alert=True)
        await CallbackQuery.answer()
        await ANJALI.pause_stream(chat_id)
        await music_off(chat_id)
        await CallbackQuery.message.reply_text(_["admin_2"].format(mention), reply_markup=close_markup(_))
    elif command == "Resume":
        if await is_music_playing(chat_id): return await CallbackQuery.answer(_["admin_3"], show_alert=True)
        await CallbackQuery.answer()
        await ANJALI.resume_stream(chat_id)
        await music_on(chat_id)
        await CallbackQuery.message.reply_text(_["admin_4"].format(mention), reply_markup=close_markup(_))
    elif command == "Stop" or command == "End":
        await CallbackQuery.answer()
        await ANJALI.stop_stream(chat_id)
        await set_loop(chat_id, 0)
        await CallbackQuery.message.reply_text(_["admin_5"].format(mention), reply_markup=close_markup(_))
        await CallbackQuery.message.delete()
    elif command == "Autoplay":
        state = await is_autoplay_on(chat_id)
        if state:
            await autoplay_off(chat_id)
            await CallbackQuery.answer("🔴 ᴧυᴛσᴘʟᴧʏ ᴅɪsᴧʙʟєᴅ!", show_alert=True)
            await CallbackQuery.message.reply_text(
                f"<blockquote><b><tg-emoji emoji-id=\"5318840353510408444\">🔴</tg-emoji> <tg-emoji emoji-id=\"6082387600599944892\">🎧</tg-emoji> ᴧυᴛσᴘʟᴧʏ sʏsᴛєϻ</b>\n\n<b>ᴧυᴛσᴘʟᴧʏ ғσʀ ᴛʜɪs ɢʀσυᴘ ɪs ησᴡ ᴅɪsᴧʙʟєᴅ <tg-emoji emoji-id=\"5318840353510408444\">🔴</tg-emoji>.</b>\n└ <b>ʙʏ :</b> {mention}</blockquote>",
                 reply_markup=close_markup(_)
            )
        else:
            await autoplay_on(chat_id)
            await CallbackQuery.answer("🟢 ᴧυᴛσᴘʟᴧʏ єηᴧʙʟєᴅ!", show_alert=True)
            await CallbackQuery.message.reply_text(
                f"<blockquote><b><tg-emoji emoji-id=\"6113685078825505075\">🟢</tg-emoji> <tg-emoji emoji-id=\"6082387600599944892\">🎧</tg-emoji> ᴧυᴛσᴘʟᴧʏ sʏsᴛєϻ</b>\n\n<b>ᴧυᴛσᴘʟᴧʏ ғσʀ ᴛʜɪs ɢʀσυᴘ ɪs ησᴡ єηᴧʙʟєᴅ <tg-emoji emoji-id=\"6113685078825505075\">🟢</tg-emoji>.</b>\n└ <b>ʙʏ :</b> {mention}</blockquote>",
                  reply_markup=close_markup(_)
            )
    elif command == "Skip" or command == "Replay":
        check = db.get(chat_id)
        if not check or len(check) == 0:
            return await CallbackQuery.answer("ǫυєυє ɪs єϻᴘᴛʏ σʀ ᴛʜє ᴘʟᴧʏʟɪsᴛ ʜᴧs ʙєєη ᴄʟєᴧʀєᴅ!", show_alert=True)

        if command == "Skip":
            txt = f"<blockquote><b><tg-emoji emoji-id=\"5850346984501680054\">▶️</tg-emoji> ➻ sᴛʀєᴧϻ sᴋɪᴘᴘєᴅ <tg-emoji emoji-id=\"6172273586703700991\">🥀</tg-emoji></b>\n│ \n└<b>ʙʏ :</b> {mention}</blockquote>"
            try:
                popped = check.pop(0)
                if popped: await auto_clean(popped)
                if not check:
                    await CallbackQuery.edit_message_text(txt)
                    await CallbackQuery.message.reply_text(_["admin_6"].format(mention, CallbackQuery.message.chat.title), reply_markup=close_markup(_))
                    return await ANJALI.stop_stream(chat_id)
            except:
                return await ANJALI.stop_stream(chat_id)
        else:
            txt = f"<blockquote><b><tg-emoji emoji-id=\"5960671702059848143\">⬅️</tg-emoji> ➻ sᴛʀєᴧϻ ʀє-ᴘʟᴧʏєᴅ <tg-emoji emoji-id=\"6172273586703700991\">🥀</tg-emoji></b>\n│ \n└<b>ʙʏ :</b> {mention}</blockquote>"

        await CallbackQuery.answer()
        queued = check[0]["file"]
        title = (check[0]["title"]).title()
        user = check[0]["by"]
        duration = check[0]["dur"]
        streamtype = check[0]["streamtype"]
        videoid = check[0]["vidid"]
        status = True if str(streamtype) == "video" else None
        db[chat_id][0]["played"] = 0

        try:
            image = await YouTube.thumbnail(videoid, True)
        except:
            image = None

        try:
            if "live_" in queued:
                n, link = await YouTube.video(videoid, True)
                if n == 0: return await CallbackQuery.message.reply_text(_["admin_7"].format(title))
                await ANJALI.skip_stream(chat_id, link, video=status, image=image)
            elif "vid_" in queued:
                 await ANJALI.skip_stream(chat_id, queued, video=status, image=image)
            else:
                 await ANJALI.skip_stream(chat_id, queued, video=status, image=image)
        except:
            return await CallbackQuery.message.reply_text(_["call_6"])

        button = stream_markup(_, chat_id)
        img = await get_thumb(videoid, CallbackQuery.from_user.id, client)
        run = await CallbackQuery.message.reply_photo(
            photo=img if img else STREAM_IMG_URL,
            caption=_["stream_1"].format(f"https://t.me/{app.username}?start=info_{videoid}", title[:23], duration, user),
            reply_markup=InlineKeyboardMarkup(button),
        )
        if chat_id in db and len(db[chat_id]) > 0:
            db[chat_id][0]["mystic"] = run
            db[chat_id][0]["markup"] = "tg"
        await CallbackQuery.edit_message_text(txt, reply_markup=close_markup(_))

async def markup_timer():
    while not await asyncio.sleep(7):
        active_chats = await get_active_chats()
        for chat_id in active_chats:
            try:
                if not await is_music_playing(chat_id): continue
                playing = db.get(chat_id)
                if not playing or int(playing[0]["seconds"]) == 0: continue
                mystic = playing[0]["mystic"]
                try:
                    if checker[chat_id][mystic.id] is False: continue
                except: pass

                try:
                    language = await get_lang(chat_id)
                    _ = get_string(language)
                except: _ = get_string("en")

                try:
                    buttons = stream_markup_timer(_, chat_id, seconds_to_min(playing[0]["played"]), playing[0]["dur"])
                    await mystic.edit_reply_markup(reply_markup=InlineKeyboardMarkup(buttons))
                except: continue
            except: continue

asyncio.create_task(markup_timer()) 

@app.on_message(filters.video & filters.private)
async def get_my_own_file_id(client, message):
    await message.reply_text(f"<blockquote><b><tg-emoji emoji-id=\"5409143496902716934\">🖼</tg-emoji> ϻєʀᴧ ᴠɪᴅєσ ғɪʟє ɪᴅ (ɪsᴋσ ᴄσᴘʏ ᴋᴧʀσ) :</b>\n<code>{message.video.file_id}</code></blockquote>")
