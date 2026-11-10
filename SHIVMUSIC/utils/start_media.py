"""Shared state for the /start video so the Back buttons can restore it."""

VIDEO_URL = "https://files.catbox.moe/0v9z4o.mp4"

# Telegram file_id of the start video. Filled in by plugins/bot/start.py after the
# first successful /start (or by the Back handler if it had to upload from URL).
cached_video_id = None
