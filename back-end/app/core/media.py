from pathlib import Path
import re
import unicodedata

BASE_DIR = Path(__file__).resolve().parents[2]
MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / "static"
IMAGE_MEDIA_DIR = STATIC_ROOT / "images"
IMAGE_STATIC_DIR = IMAGE_MEDIA_DIR
AUDIO_MEDIA_DIR = MEDIA_ROOT / "audio"


def ensure_media_directories() -> None:
    MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
    STATIC_ROOT.mkdir(parents=True, exist_ok=True)
    IMAGE_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    AUDIO_MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    normalized = re.sub(r"[^a-zA-Z0-9]+", "-", normalized).strip("-").lower()
    return normalized or "word"


def word_media_stem(word) -> str:
    identifier = getattr(word, "id", None)
    word_value = getattr(word, "word", "word")
    if identifier is not None:
        return slugify(f"{identifier}-{word_value}")
    return slugify(word_value)


def media_url(kind: str, filename: str) -> str:
    if kind == "images":
        return f"/static/images/{filename}"
    return f"/media/{kind}/{filename}"
