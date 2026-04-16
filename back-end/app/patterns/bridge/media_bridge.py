from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen
import json

from app.core.config import settings
from app.core.media import AUDIO_MEDIA_DIR, ensure_media_directories, media_url, word_media_stem
from app.patterns.adapter.pexels_adapter import StandardImage
from app.patterns.proxy.image_service_proxy import ImageServiceProxy


@dataclass
class StandardAudio:
    id: str
    url: str
    local_path: Path | None = None
    source_url: str | None = None


@dataclass
class VocabularyMediaAsset:
    image: StandardImage
    audio: StandardAudio | None


class ImageProvider(ABC):
    @abstractmethod
    def provide(self, word) -> StandardImage:
        raise NotImplementedError


class AudioProvider(ABC):
    @abstractmethod
    def provide(self, word) -> StandardAudio | None:
        raise NotImplementedError


class PexelsImageProvider(ImageProvider):
    def __init__(self, proxy: ImageServiceProxy | None = None):
        self.proxy = proxy or ImageServiceProxy()

    def provide(self, word) -> StandardImage:
        result = self.proxy.fetch(word)
        return result.standard_image


class DictionaryApiAudioProvider(AudioProvider):
    def provide(self, word) -> StandardAudio | None:
        ensure_media_directories()
        stem = word_media_stem(word)
        cached_path = AUDIO_MEDIA_DIR / f"{stem}.mp3"
        if cached_path.exists() and cached_path.stat().st_size > 0:
            return StandardAudio(
                id=stem,
                url=media_url("audio", cached_path.name),
                local_path=cached_path,
                source_url=None,
            )

        audio_url = self._resolve_dictionary_audio_url(getattr(word, "word", ""))
        if not audio_url:
            return None

        audio_bytes = self._download_bytes(audio_url)
        cached_path.write_bytes(audio_bytes)
        return StandardAudio(
            id=stem,
            url=media_url("audio", cached_path.name),
            local_path=cached_path,
            source_url=audio_url,
        )

    def _resolve_dictionary_audio_url(self, word_text: str) -> str | None:
        if not word_text:
            return None

        base_url = settings.dictionary_api_base_url.rstrip("/")
        request_url = f"{base_url}/entries/en/{quote_plus(word_text)}"
        request = Request(
            request_url,
            headers={"Accept": "application/json"},
        )

        try:
            with urlopen(request, timeout=25) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError, OSError, ValueError):
            return None

        for entry in payload or []:
            for phonetic in entry.get("phonetics", []):
                audio = phonetic.get("audio")
                if audio:
                    return audio
        return None

    def _download_bytes(self, url: str) -> bytes:
        if url.startswith("//"):
            url = f"https:{url}"

        request = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
                )
            },
        )
        with urlopen(request, timeout=30) as response:
            return response.read()


class VocabularyMedia:
    def __init__(self, image_provider: ImageProvider, audio_provider: AudioProvider):
        self.image_provider = image_provider
        self.audio_provider = audio_provider

    def build(self, word) -> VocabularyMediaAsset:
        image = self.image_provider.provide(word)
        audio = self.audio_provider.provide(word)
        return VocabularyMediaAsset(image=image, audio=audio)