import random
from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import config
from SHIVMUSIC import app
from SHIVMUSIC.misc import SUDOERS
from pyrogram.enums import ButtonStyle

def get_style_map():
    return {1: ButtonStyle.PRIMARY, 2: ButtonStyle.PRIMARY, 3: ButtonStyle.PRIMARY}

def create_btn(text, cb=None, url=None, style=ButtonStyle.PRIMARY, no_emoji=True):
    kwargs = {"text": text, "style": style}
    if cb is not None:
        kwargs["callback_data"] = cb
    if url is not None:
        kwargs["url"] = url
    return InlineKeyboardButton(**kwargs)


# Help pages that only the bot owner / sudo users may see.
# hb3 = G-CAST (broadcast), hb4 = BL-CHAT, hb5 = BL-USER, hb7 = G-BAN
OWNER_ONLY_HELP = {"hb3", "hb4", "hb5", "hb7"}


def is_owner_user(user_id) -> bool:
    """True only for the configured owner or users in SUDOERS."""
    try:
        if not user_id:
            return False
        if config.OWNER_ID and int(user_id) == int(config.OWNER_ID):
            return True
        return int(user_id) in SUDOERS
    except Exception:
        return False


def help_pannel(_, START: Union[bool, int] = None, is_owner: bool = False):
    """Normal users get the basic commands; owner/sudo also get admin options."""
    s_map = get_style_map()
    buttons = []
    for i in range(1, 16):
        key = f"hb{i}"
        owner_only = key in OWNER_ONLY_HELP
        if owner_only and not is_owner:
            continue
        buttons.append(
            create_btn(
                text=_[f"H_B_{i}"],
                cb=f"help_callback {key}",
                style=ButtonStyle.DANGER if owner_only else s_map[3],
            )
        )
    rows = [buttons[i:i + 3] for i in range(0, len(buttons), 3)]
    rows.append([create_btn(text=_["BACK_BUTTON"], cb="settingsback_helper", style=s_map[1])])
    return InlineKeyboardMarkup(rows)


def first_page(_, is_owner: bool = False):
    s_map = get_style_map()
    first = [
        [
            create_btn(text=_["H_B_1"], cb="help_callback hb1", style=s_map[3]),
            create_btn(text=_["H_B_2"], cb="help_callback hb2", style=s_map[3]),
            create_btn(text=_["H_B_3"], cb="help_callback hb3", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_11"], cb="help_callback hb11", style=s_map[3]),
            create_btn(text=_["H_B_8"], cb="help_callback hb8", style=s_map[3]),
            create_btn(text=_["H_B_6"], cb="help_callback hb6", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_13"], cb="help_callback hb13", style=s_map[3]),
            create_btn(text=_["H_B_12"], cb="help_callback hb12", style=s_map[3]),
            create_btn(text=_["H_B_9"], cb="help_callback cloghelp", style=s_map[3]),
        ],
        [
            create_btn(text=_["H_B_10"], cb="help_callback hb10", style=s_map[3]),
            create_btn(text=_["H_B_14"], cb="help_callback hb14", style=s_map[3]),
            create_btn(text=_["H_B_15"], cb="help_callback hb15", style=s_map[3]),
        ],
    ]
    
    first.append([create_btn(text=_["BACK_BUTTON"], cb="settingsback_home", style=s_map[1])])
    return InlineKeyboardMarkup(first)


def help_back_markup(_):
    s_map = get_style_map()
    return InlineKeyboardMarkup([
        [create_btn(text=_["BACK_BUTTON"], cb="help_home", style=s_map[1])]
    ])


def private_help_panel(_):
    s_map = get_style_map()
    return InlineKeyboardMarkup([
        [create_btn(text=_["S_B_4"], url=f"https://t.me/{app.username}?start=help", style=s_map[1])]
    ])
