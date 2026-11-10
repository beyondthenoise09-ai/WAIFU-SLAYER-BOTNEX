import html


def escape_html(text: str) -> str:
    if not text:
        return ""
    return html.escape(str(text))


def build_welcome_html(user_mention: str, bot_mention: str, bot_username: str | None = None) -> str:
    return (
        f"❖✦ ʜᴇʏ {user_mention} !\n"
        f"❖✦ ᴛʜɪs ɪs 🎀 {bot_mention} 🎀 ⋆ ࣪ 𝜗𝜚\n\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"❖ 🎧 ʜɪɢʜ-ǫᴜᴀʟɪᴛʏ ᴠᴄ ᴍᴜsɪᴄ ᴘʟᴀʏᴇʀ ʙᴏᴛ\n"
        f"❖ ⚡ 24x7 ᴀᴄᴛɪᴠᴇ | 💎 ᴘʀᴇᴍɪᴜᴍ ǫᴜᴀʟɪᴛʏ\n"
        f"❖ 🎶 ʟᴀɢ-ғʀᴇᴇ ʜᴅ ᴀᴜᴅɪᴏ sᴛʀᴇᴀᴍɪɴɢ\n\n"
        f"❖ ❓ ᴄʟɪᴄᴋ ᴏɴ ᴛʜᴇ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ᴛᴏ ɢᴇᴛ ɪɴғᴏ\n"
        f"ᴀʙᴏᴜᴛ ᴍʏ ᴍᴏᴅᴜʟᴇs ᴀɴᴅ ᴄᴏᴍᴍᴀɴᴅs...!\n"
        f"➖➖➖➖➖➖➖➖➖➖"
    )
