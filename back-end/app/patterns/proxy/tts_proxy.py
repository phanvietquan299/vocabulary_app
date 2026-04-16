from abc import ABC, abstractmethod
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus
from urllib.request import Request, urlopen

from app.core.media import ensure_media_directories


class TTSSubject(ABC):
    @abstractmethod
    def generate(self, word_text: str, output_path: Path) -> Path:
        raise NotImplementedError


class GoogleTTSAudioSubject(TTSSubject):
    def generate(self, word_text: str, output_path: Path) -> Path:
        ensure_media_directories()
        query = quote_plus(word_text)
        url = (
            "https://translate.google.com/translate_tts"
            f"?ie=UTF-8&q={query}&tl=en&client=tw-ob"
        )
        request = Request(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
                ),
                "Accept": "audio/mpeg",
            },
        )

        with urlopen(request, timeout=25) as response:
            audio_bytes = response.read()

        output_path.write_bytes(audio_bytes)
        return output_path


class CachedTTSAudioProxy(TTSSubject):
    def __init__(self, real_subject: TTSSubject | None = None):
        self.real_subject = real_subject or GoogleTTSAudioSubject()

    def generate(self, word_text: str, output_path: Path) -> Path:
        ensure_media_directories()
        if output_path.exists() and output_path.stat().st_size > 0:
            return output_path

        try:
            return self.real_subject.generate(word_text, output_path)
        except (HTTPError, URLError, TimeoutError, OSError):
            raise
