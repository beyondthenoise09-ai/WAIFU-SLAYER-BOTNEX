"""Start, support and about keyboards for WAIFU-SLAYER (BOTNEX premium UI)."""

from pyrogram.types import InlineKeyboardButton
from pyrogram.enums import ButtonStyle
import config
from SHIVMUSIC import app


def create_btn(text, cb=None, url=None, user_id=None, style=ButtonStyle.PRIMARY, no_emoji=True):
    kwargs = {"text": text, "style": style}
    if cb is not None:
        kwargs["callback_data"] = cb
    if url is not None:
        kwargs["url"] = url
    if user_id is not None:
        kwargs["user_id"] = user_id
    return InlineKeyboardButton(**kwargs)


def _group_link() -> str:
    """Support group: env SUPPORT_CHAT if set, otherwise the BOTNEX group."""
    return config.SUPPORT_CHAT or config.BOTNEX_GROUP_LINK


def _updates_link() -> str:
    """Updates: env SUPPORT_CHANNEL if set, otherwise the BOTNEX group."""
    return config.SUPPORT_CHANNEL or config.BOTNEX_GROUP_LINK


def start_panel(_):
    buttons = [
        [
            create_btn("➕ ADD TO GROUP", url=f"https://t.me/{app.username}?startgroup=true", style=ButtonStyle.SUCCESS),
            create_btn("⌘ COMMANDS", url=f"https://t.me/{app.username}?start=help"),
        ]
    ]
    return buttons


def private_panel(_):
    buttons = [
        [
            create_btn(
                "🎧➕ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ➕🎧",
                url=f"https://t.me/{app.username}?startgroup=true",
                style=ButtonStyle.PRIMARY,
            )
        ],
        [
            create_btn("✨ ᴀʙᴏᴜᴛ 🪩", cb="gib_source", style=ButtonStyle.SUCCESS),
            create_btn("💎 ɪɴғᴏ 🏛", cb="botnex_info", style=ButtonStyle.SUCCESS),
        ],
        [
            create_btn("👑 ᴏᴡɴᴇʀ 🎀", url=config.BOTNEX_OWNER_LINK, style=ButtonStyle.SUCCESS),
            create_btn("🚀 ᴜᴘᴅᴀᴛᴇs ↗", url=_updates_link(), style=ButtonStyle.SUCCESS),
        ],
        [create_btn("🎵 ʜᴇʟᴘ ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs 🎵", cb="help_home", style=ButtonStyle.PRIMARY)],
        [
            create_btn("💬 sᴜᴘᴘᴏʀᴛ", cb="support_page", style=ButtonStyle.PRIMARY),
            create_btn("🌐 ʟᴀɴɢᴜᴀɢᴇ", cb="LG", style=ButtonStyle.PRIMARY),
        ],
    ]
    return buttons


def support_panel(_):
    links = [create_btn("💬 ᴊᴏɪɴ ɢʀᴏᴜᴘ", url=_group_link())]
    if config.SUPPORT_CHANNEL:
        links.append(create_btn("🚀 ᴜᴘᴅᴀᴛᴇs ↗", url=config.SUPPORT_CHANNEL))
    buttons = [links]
    buttons.append([create_btn("‹ BACK", cb="settingsback_helper")])
    return buttons


def about_panel(_):
    buttons = [
        [
            create_btn("💬 ᴏᴜʀ ɢʀᴏᴜᴘ", url=config.BOTNEX_GROUP_LINK, style=ButtonStyle.SUCCESS),
            create_btn("👑 ᴏᴡɴᴇʀ", url=config.BOTNEX_OWNER_LINK, style=ButtonStyle.SUCCESS),
        ]
    ]
    if config.GITHUB and config.GITHUB.startswith("https://"):
        buttons.append([create_btn("⌘ PROJECT SOURCE", url=config.GITHUB)])
    buttons.append([create_btn("‹ BACK", cb="settingsback_helper")])
    return buttons
