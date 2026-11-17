# --- ffmpeg/ffprobe fallback for hosts without root (no apt-get / no Dockerfile) ---
import os as _os
import shutil as _shutil
import sys as _sys


def _ensure_ffmpeg():
    if _shutil.which("ffmpeg") and _shutil.which("ffprobe"):
        return
    import platform
    import tarfile
    import tempfile
    import urllib.request

    if not _sys.platform.startswith("linux") or platform.machine().lower() not in ("x86_64", "amd64"):
        return

    url = _os.getenv(
        "FFMPEG_DOWNLOAD_URL",
        "https://johnvansickle.com/ffmpeg/releases/ffmpeg-release-amd64-static.tar.xz",
    )
    bin_dir = None
    for base in (_os.path.expanduser("~"), tempfile.gettempdir()):
        try:
            candidate = _os.path.join(base, ".botnex_ffmpeg")
            _os.makedirs(candidate, exist_ok=True)
            if _os.access(candidate, _os.W_OK):
                bin_dir = candidate
                break
        except Exception:
            continue
    if not bin_dir:
        return

    ffmpeg_path = _os.path.join(bin_dir, "ffmpeg")
    ffprobe_path = _os.path.join(bin_dir, "ffprobe")
    if not (_os.path.exists(ffmpeg_path) and _os.path.exists(ffprobe_path)):
        print("[INFO] ffmpeg not found on host, downloading static build (one time)...")
        with urllib.request.urlopen(url, timeout=120) as resp:
            with tarfile.open(fileobj=resp, mode="r|xz") as tar:
                for member in tar:
                    name = _os.path.basename(member.name)
                    if member.isfile() and name in ("ffmpeg", "ffprobe"):
                        src = tar.extractfile(member)
                        with open(_os.path.join(bin_dir, name), "wb") as out:
                            _shutil.copyfileobj(src, out)
                        _os.chmod(_os.path.join(bin_dir, name), 0o755)
        print("[INFO] ffmpeg/ffprobe ready.")
    _os.environ["PATH"] = bin_dir + _os.pathsep + _os.environ.get("PATH", "")


try:
    _ensure_ffmpeg()
except Exception as _ffmpeg_err:
    print(f"[WARN] ffmpeg setup skipped: {_ffmpeg_err}")
# -----------------------------------------------------------------------------

from SHIVMUSIC.core.bot import ANJALI
from SHIVMUSIC.core.dir import dirr
from SHIVMUSIC.core.git import git
from SHIVMUSIC.core.userbot import Userbot
from SHIVMUSIC.misc import dbb, heroku
from pyrogram import Client
from SafoneAPI import SafoneAPI
from .logging import LOGGER

dirr()
git()
dbb()
heroku()

app = ANJALI()
api = SafoneAPI()
userbot = Userbot()

from .platforms import *

Apple = AppleAPI()
Carbon = CarbonAPI()
SoundCloud = SoundAPI()
Spotify = SpotifyAPI()
Resso = RessoAPI()
Telegram = TeleAPI()
YouTube = YouTubeAPI()
