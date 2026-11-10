# WAIFU-SLAYER · BOTNEX Update

This update keeps the existing REDWINE-based playback and AutoPlay architecture in place while refreshing the user-facing presentation.

## Included

- Reworked private and group welcome presentation with WAIFU-SLAYER / BOTNEX identity.
- Cleaner start, commands, language, support and about button layout using existing callback handlers.
- Branded support and about panels.
- Refined voice-chat player controls with consistent button styling; stop remains visually distinct.
- BOTNEX footer on English now-playing and live-stream messages.
- Corrected the AutoPlay cookie-assets directory lookup to point at `SHIVMUSIC/assets`.
- Removed Python bytecode/cache files from the release archive.

## Preserved

- Existing playback and queue implementation.
- Existing AutoPlay related-track discovery and fallback search logic.
- Existing database, assistant, platform and command modules.
- Original upstream license file.

## Validation

- Python syntax parsed successfully across the project.
- All bundled language YAML files parsed successfully.
- No live Telegram voice-chat, Railway deployment, or playback session was run as part of this packaging step. Configure your own environment variables and test in a private group before production use.

---

## Premium UI Update v2 (Phase 1-4)

- **Phase 1** - Back button now restores the start VIDEO (old code replaced it with the Neon `upic.png`). Fix: `plugins/admins/callback.py` + new `utils/start_media.py`.
- **Phase 2** - Player panels: `[ 🎧 AUTOPLAY ] [ 💎 SUPPORT ]` row, red Close. Callback data unchanged. File: `utils/inline/play.py`.
- **Phase 3** - Help menu: G-CAST, BL-CHAT, BL-USER, G-BAN visible only to owner/sudo, plus a server-side check in `helper_cb`. Files: `utils/inline/help.py`, `plugins/bot/help.py`, `plugins/bot/start.py`.
- **Phase 4** - Skipped on request: the original thumbnail design (`utils/thumbnails.py`) is kept exactly as it was.
- Start menu: Add / About / Info / Owner / Updates / Help; About + Info panels with the community group link; Owner button uses the public username only.
- Add-to-group log card now uses https://files.catbox.moe/f3kqmo.png (text fallback if the photo fails).

Not changed: playback core, platforms, database, requirements, Procfile, Dockerfile.
Not verified here: live Telegram, voice chat playback, Railway deploy.
