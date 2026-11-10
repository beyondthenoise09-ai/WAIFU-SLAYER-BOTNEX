from typing import Union
import random
from SHIVMUSIC import app
import config
from SHIVMUSIC.utils.formatters import time_to_seconds
from pyrogram.enums import ButtonStyle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_style_map():
    return {1: ButtonStyle.PRIMARY, 2: ButtonStyle.PRIMARY, 3: ButtonStyle.DANGER}

def create_btn(text, cb=None, url=None, user_id=None, style=ButtonStyle.PRIMARY, no_emoji=True):
    kwargs = {"text": text, "style": style}
    if cb is not None:
        kwargs["callback_data"] = cb
    if url is not None:
        kwargs["url"] = url
    if user_id is not None:
        kwargs["user_id"] = user_id
    return InlineKeyboardButton(**kwargs)


def queue_markup(
    _,
    DURATION,
    CPLAY,
    videoid,
    played: Union[bool, int] = None,
    dur: Union[bool, int] = None,
):
    s_map = get_style_map()
    not_dur = [
        [
            create_btn(
                text=_["QU_B_1"],
                cb=f"GetQueued {CPLAY}|{videoid}",
                style=s_map[1]
            ),
            create_btn(
                text=_["CLOSE_BUTTON"],
                cb="close",
                style=s_map[1]
            ),
        ]
    ]
    dur_buttons = [
        [
            create_btn(
                text=_["QU_B_2"].format(played, dur),
                cb="GetTimer",
                style=s_map[1],
                no_emoji=False
            )
        ],
        [
            create_btn(
                text=_["QU_B_1"],
                cb=f"GetQueued {CPLAY}|{videoid}",
                style=s_map[2]
            ),
            create_btn(
                text=_["CLOSE_BUTTON"],
                cb="close",
                style=s_map[2]
            ),
        ],
    ]
    upl = InlineKeyboardMarkup(not_dur if DURATION == "Unknown" else dur_buttons)
    return upl


def queue_back_markup(_, CPLAY):
    s_map = get_style_map()
    upl = InlineKeyboardMarkup(
        [
            [
                create_btn(
                    text=_["BACK_BUTTON"],
                    cb=f"queue_back_timer {CPLAY}",
                    style=s_map[1]
                ),
                create_btn(
                    text=_["CLOSE_BUTTON"],
                    cb="close",
                    style=s_map[1]
                ),
            ]
        ]
    )
    return upl


def aq_markup(_, chat_id):
    s_map = get_style_map()
    buttons = [
        [
            create_btn(text="▷", cb=f"ADMIN Resume|{chat_id}", style=s_map[1], no_emoji=False),
            create_btn(text="II", cb=f"ADMIN Pause|{chat_id}", style=s_map[1], no_emoji=False),
            create_btn(text="↻", cb=f"ADMIN Replay|{chat_id}", style=s_map[1], no_emoji=False),
            create_btn(text="‣‣I", cb=f"ADMIN Skip|{chat_id}", style=s_map[1], no_emoji=False),
            create_btn(text="▢", cb=f"ADMIN Stop|{chat_id}", style=s_map[1], no_emoji=False),
        ],
        [
            create_btn(
                text=_["CLOSE_BUTTON"],
                cb="close",
                style=s_map[2]
            ),
        ],
    ]
    return buttons


def queuemarkup(_, vidid, chat_id):
    s_map = get_style_map()
    
    buttons = [
        [
            create_btn(
                text=_["S_B_5"],
                url=f"https://t.me/{app.username}?startgroup=true",
                style=s_map[1]
            ),
        ],
        [
            create_btn(text="ᴘᴀᴜsᴇ", cb=f"ADMIN Pause|{chat_id}", style=s_map[2]),
            create_btn(text="sᴛᴏᴘ", cb=f"ADMIN Stop|{chat_id}", style=s_map[2]),
            create_btn(text="sᴋɪᴘ", cb=f"ADMIN Skip|{chat_id}", style=s_map[2]),
        ],
        [
            create_btn(text="ʀᴇsᴜᴍᴇ", cb=f"ADMIN Resume|{chat_id}", style=s_map[3]),
            create_btn(text="ʀᴇᴘʟᴀʏ", cb=f"ADMIN Replay|{chat_id}", style=s_map[3]),
        ],
        [
            create_btn(
                text="ᴍᴏʀᴇ",
                url=config.SUPPORT_CHANNEL or f"https://t.me/{app.username}",
                style=s_map[1]
            ),
        ],
    ]

    return buttons
