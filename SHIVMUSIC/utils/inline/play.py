import math
import random

from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton

from config import SUPPORT_CHAT, OWNER_USERNAME
from SHIVMUSIC import app
import config
from SHIVMUSIC.utils.formatters import time_to_seconds

# Native symbols keep controls visible on every Telegram client.
PLAY_EMOJI = "▶"
PAUSE_EMOJI = "Ⅱ"
REPLAY_EMOJI = "↻"
SKIP_EMOJI = "⏭"
STOP_EMOJI = "■"
EQ_EMOJI = "🎚"

def get_style_map():
    return {1: ButtonStyle.PRIMARY, 2: ButtonStyle.PRIMARY, 3: ButtonStyle.DANGER, 4: ButtonStyle.SUCCESS}

def create_btn(text, cb=None, url=None, style=ButtonStyle.PRIMARY, emoji_id=None, no_emoji=True):
    kwargs = {"text": text, "style": style}
    if cb is not None:
        kwargs["callback_data"] = cb
    if url is not None:
        kwargs["url"] = url
    return InlineKeyboardButton(**kwargs)


def _support_url():
    return config.SUPPORT_CHAT or config.BOTNEX_GROUP_LINK


def _premium_row(chat_id):
    """[ 🎧 AUTOPLAY ] [ 💎 SUPPORT ] row used on every player panel."""
    return [
        create_btn(text="🎧 AUTOPLAY", cb=f"ADMIN Autoplay|{chat_id}", style=ButtonStyle.SUCCESS),
        create_btn(text="💎 SUPPORT", url=_support_url(), style=ButtonStyle.PRIMARY),
    ]

# --- MARKUP FUNCTIONS ---

def track_markup(_, videoid, user_id, channel, fplay):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["P_B_1"], cb=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}", style=s_map[2]),
            create_btn(text=_["P_B_2"], cb=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}", style=s_map[2]),
        ],
        [
            create_btn(text=_["CLOSE_BUTTON"], cb=f"forceclose {videoid}|{user_id}", style=s_map[2])
        ],
    ]
    return buttons


def stream_markup_timer(_, chat_id, played, dur):
    try:
        played_sec = time_to_seconds(str(played))
        duration_sec = 0 if str(dur).lower() in ["live", "unknown", "0"] else time_to_seconds(str(dur))
    except Exception:
        played_sec = 0
        duration_sec = 0

    total_blocks = 10
    filled_blocks = int((played_sec / duration_sec) * total_blocks) if duration_sec > 0 else 0
    filled_blocks = min(max(filled_blocks, 0), total_blocks - 1)
    bar = "▰" * filled_blocks + "◆" + "▱" * (total_blocks - filled_blocks - 1)

    s_map = get_style_map()
    return [
        [create_btn(text=f"{played}  {bar}  {dur}", cb="GetTimer", style=s_map[1])],
        [
            create_btn(text="▶", cb=f"ADMIN Resume|{chat_id}", style=s_map[1]),
            create_btn(text="Ⅱ", cb=f"ADMIN Pause|{chat_id}", style=s_map[1]),
            create_btn(text="🎚", cb=f"EqPanel {chat_id}", style=s_map[1]),
            create_btn(text="⏭", cb=f"ADMIN Skip|{chat_id}", style=s_map[1]),
            create_btn(text="■", cb=f"ADMIN Stop|{chat_id}", style=s_map[3]),
        ],
        _premium_row(chat_id),
        [create_btn(text=_["CLOSE_BUTTON"], cb="close", style=ButtonStyle.DANGER)],
    ]


def stream_markup(_, chat_id):
    s_map = get_style_map()
    return [
        [
            create_btn(text="▶", cb=f"ADMIN Resume|{chat_id}", style=s_map[1]),
            create_btn(text="Ⅱ", cb=f"ADMIN Pause|{chat_id}", style=s_map[1]),
            create_btn(text="🎚", cb=f"EqPanel {chat_id}", style=s_map[1]),
            create_btn(text="⏭", cb=f"ADMIN Skip|{chat_id}", style=s_map[1]),
            create_btn(text="■", cb=f"ADMIN Stop|{chat_id}", style=s_map[3]),
        ],
        _premium_row(chat_id),
        [create_btn(text=_["CLOSE_BUTTON"], cb="close", style=ButtonStyle.DANGER)],
    ]


def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["P_B_1"], cb=f"ANJALIPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}", style=s_map[2]),
            create_btn(text=_["P_B_2"], cb=f"ANJALIPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}", style=s_map[2]),
        ],
        [
            create_btn(text=_["CLOSE_BUTTON"], cb=f"forceclose {videoid}|{user_id}", style=s_map[2])
        ],
    ]
    return buttons


def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["P_B_3"], cb=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}", style=s_map[1]),
        ],
        [
            create_btn(text=_["CLOSE_BUTTON"], cb=f"forceclose {videoid}|{user_id}", style=s_map[2])
        ],
    ]
    return buttons


def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = f"{query[:20]}"
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["P_B_1"], cb=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}", style=s_map[2]),
            create_btn(text=_["P_B_2"], cb=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}", style=s_map[2]),
        ],
        [
            create_btn(text="ʙᴀᴄᴋ", cb=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}", style=s_map[3]),
            create_btn(text=_["CLOSE_BUTTON"], cb=f"forceclose {query}|{user_id}", style=s_map[3]),
            create_btn(text="ɴᴇxᴛ", cb=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}", style=s_map[3]),
        ],
    ]
    return buttons


def telegram_markup(_, chat_id):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text="ɴᴇxᴛ", cb=f"PanelMarkup None|{chat_id}", style=s_map[1]),
            create_btn(text=_["CLOSEMENU_BUTTON"], cb="close", style=s_map[2]),
        ],
    ]
    return buttons


def queue_markup(_, videoid, chat_id):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["S_B_3"], url=f"https://t.me/{app.username}?startgroup=true", style=s_map[1]),
        ],
        [
            create_btn(text="▶", cb=f"ADMIN Resume|{chat_id}", style=s_map[3], emoji_id=PLAY_EMOJI),
            create_btn(text="Ⅱ", cb=f"ADMIN Pause|{chat_id}", style=s_map[3], emoji_id=PAUSE_EMOJI),
            create_btn(text="🎚", cb=f"EqPanel {chat_id}", style=s_map[3], emoji_id=EQ_EMOJI),
            create_btn(text="⏭", cb=f"ADMIN Skip|{chat_id}", style=s_map[3], emoji_id=SKIP_EMOJI),
            create_btn(text="■", cb=f"ADMIN Stop|{chat_id}", style=s_map[3], emoji_id=STOP_EMOJI),
        ],
        _premium_row(chat_id),
        [
            create_btn(text="ᴍᴏʀᴇ", cb=f"PanelMarkup None|{chat_id}", style=s_map[1]),
        ],
    ]
    return buttons


def stream_markup2(_, chat_id):
    return stream_markup(_, chat_id)


def stream_markup_timer2(_, chat_id, played, dur):
    return stream_markup_timer(_, chat_id, played, dur)


def panel_markup_1(_, videoid, chat_id):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["S_B_3"], url=f"https://t.me/{app.username}?startgroup=true", style=s_map[1]),
        ],
        [
            create_btn(text="sʜᴜғғʟᴇ", cb=f"ADMIN Shuffle|{chat_id}", style=s_map[3]),
            create_btn(text="ʟᴏᴏᴘ", cb=f"ADMIN Loop|{chat_id}", style=s_map[3]),
        ],
        [
            create_btn(text="-10 sᴇᴄ", cb=f"ADMIN 1|{chat_id}", style=s_map[2]),
            create_btn(text="+10 sᴇᴄ", cb=f"ADMIN 2|{chat_id}", style=s_map[2]),
        ],
        _premium_row(chat_id),
        [
            create_btn(text="ʜᴏᴍᴇ", cb=f"Pages Back|2|{videoid}|{chat_id}", style=s_map[2]),
            create_btn(text="ɴᴇxᴛ", cb=f"Pages Forw|2|{videoid}|{chat_id}", style=s_map[2]),
        ],
    ]
    return buttons


def panel_markup_2(_, videoid, chat_id):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["S_B_3"], url=f"https://t.me/{app.username}?startgroup=true", style=s_map[1]),
        ],
        [
            create_btn(text="0.5x", cb=f"SpeedUP {chat_id}|0.5", style=s_map[3]),
            create_btn(text="0.75x", cb=f"SpeedUP {chat_id}|0.75", style=s_map[3]),
            create_btn(text="1.0x", cb=f"SpeedUP {chat_id}|1.0", style=s_map[3]),
        ],
        [
            create_btn(text="1.5x", cb=f"SpeedUP {chat_id}|1.5", style=s_map[2]),
            create_btn(text="2.0x", cb=f"SpeedUP {chat_id}|2.0", style=s_map[2]),
        ],
        [
            create_btn(text="ʙᴀᴄᴋ", cb=f"Pages Back|1|{videoid}|{chat_id}", style=s_map[1]),
        ],
    ]
    return buttons


def panel_markup_5(_, videoid, chat_id):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=_["S_B_3"], url=f"https://t.me/{app.username}?startgroup=true", style=s_map[1]),
        ],
        [
            create_btn(text="▶", cb=f"ADMIN Resume|{chat_id}", style=s_map[3], emoji_id=PLAY_EMOJI),
            create_btn(text="Ⅱ", cb=f"ADMIN Pause|{chat_id}", style=s_map[3], emoji_id=PAUSE_EMOJI),
            create_btn(text="🎚", cb=f"EqPanel {chat_id}", style=s_map[3], emoji_id=EQ_EMOJI),
            create_btn(text="⏭", cb=f"ADMIN Skip|{chat_id}", style=s_map[3], emoji_id=SKIP_EMOJI),
            create_btn(text="■", cb=f"ADMIN Stop|{chat_id}", style=s_map[3], emoji_id=STOP_EMOJI),
        ],
        _premium_row(chat_id),
        [
            create_btn(text="ʜᴏᴍᴇ", cb=f"MainMarkup {videoid}|{chat_id}", style=s_map[2]),
            create_btn(text="ɴᴇxᴛ", cb=f"Pages Forw|1|{videoid}|{chat_id}", style=s_map[2]),
        ],
    ]
    return buttons


def panel_markup_3(_, videoid, chat_id):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text="0.5x", cb=f"SpeedUP {chat_id}|0.5", style=s_map[3]),
            create_btn(text="0.75x", cb=f"SpeedUP {chat_id}|0.75", style=s_map[3]),
            create_btn(text="1.0x", cb=f"SpeedUP {chat_id}|1.0", style=s_map[3]),
        ],
        [
            create_btn(text="1.5x", cb=f"SpeedUP {chat_id}|1.5", style=s_map[2]),
            create_btn(text="2.0x", cb=f"SpeedUP {chat_id}|2.0", style=s_map[2]),
        ],
        [
            create_btn(text="ʙᴀᴄᴋ", cb=f"Pages Back|2|{videoid}|{chat_id}", style=s_map[1]),
        ],
    ]
    return buttons


def panel_markup_4(_, vidid, chat_id, played, dur):
    try:
        played_sec = time_to_seconds(str(played))
        if str(dur).lower() in ["live", "unknown", "0"]:
            duration_sec = 0
        else:
            duration_sec = time_to_seconds(str(dur))
    except Exception:
        played_sec = 0
        duration_sec = 0
    
    total_blocks = 10
    if duration_sec > 0:
        filled_blocks = int((played_sec / duration_sec) * total_blocks)
    else:
        filled_blocks = 0
        
    # Block and Moving Emoji Logic (▰▰▰🎵▱▱▱▱▱▱)
    filled_blocks = min(max(filled_blocks, 0), total_blocks - 1)
    bar = "▰" * filled_blocks + "🎵" + "▱" * (total_blocks - filled_blocks - 1)

    s_map = get_style_map()
    buttons = [
        [
            create_btn(text=f"{played} {bar} {dur}", cb="GetTimer", style=s_map[1], emoji_id=5217933090483098080)
        ],
        [
            create_btn(text="▶", cb=f"ADMIN Resume|{chat_id}", style=s_map[3], emoji_id=PLAY_EMOJI),
            create_btn(text="Ⅱ", cb=f"ADMIN Pause|{chat_id}", style=s_map[3], emoji_id=PAUSE_EMOJI),
            create_btn(text="🎚", cb=f"EqPanel {chat_id}", style=s_map[3], emoji_id=EQ_EMOJI),
            create_btn(text="⏭", cb=f"ADMIN Skip|{chat_id}", style=s_map[3], emoji_id=SKIP_EMOJI),
            create_btn(text="■", cb=f"ADMIN Stop|{chat_id}", style=s_map[3], emoji_id=STOP_EMOJI),
        ],
        _premium_row(chat_id),
        [
            create_btn(text="ʜᴏᴍᴇ", cb=f"MainMarkup {vidid}|{chat_id}", style=s_map[1]),
        ],
    ]
    return buttons
