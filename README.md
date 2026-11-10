<h1 align="center">WAIFU-SLAYER</h1>
<p align="center"><b>BOTNEX #001</b> · Telegram Voice Chat Music Bot</p>

WAIFU-SLAYER is a Telegram group voice-chat music bot with music streaming, queue management, related-track AutoPlay, equalizer presets, and playback controls.

## Configuration

1. Copy `sample.env` to `.env` (or add the same variables to your Railway service variables).
2. Set your own `API_ID`, `API_HASH`, `BOT_TOKEN`, `MONGO_DB_URI`, `OWNER_ID`, and assistant `STRING_SESSION` value(s).
3. Set `LOGGER_ID` to a private Telegram group where your bot and assistant accounts can send messages.
4. Optionally set `SUPPORT_CHAT`, `SUPPORT_CHANNEL`, `GITHUB`, and API provider credentials.
5. Never upload `.env`, bot tokens, API keys, or Telegram session strings to GitHub.

`OWNER_ID` and `SUDOERS` are intentionally not pre-filled with another developer's Telegram IDs. Support, updates, source, and logger destinations must be configured by the operator. Assistant accounts are not automatically added to unrelated third-party channels.

## Run

```bash
python -m pip install -r requirements.txt
python -m SHIVMUSIC
```

For Railway, connect your private GitHub repository, select the Python runtime, install dependencies from `requirements.txt`, and use `python -m SHIVMUSIC` as the start command. Ensure FFmpeg is available in the build/runtime environment.

## Project identity

**WAIFU-SLAYER · Powered by BOTNEX**  
**Developed & customized by Chandan.**

The original project license and upstream attribution are retained in `LICENSE`.
