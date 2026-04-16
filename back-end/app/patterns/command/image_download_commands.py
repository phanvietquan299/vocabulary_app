from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen
from mimetypes import guess_extension

from app.core.database import SessionLocal
from app.core.media import IMAGE_MEDIA_DIR, ensure_media_directories, media_url, slugify
from app.models.vocabulary_model import VocabularyModel


@dataclass
class ImageDownloadContext:
    word_id: int
    word: str
    remote_url: str
    local_url: str | None = None
    local_path: Path | None = None


class DownloadImageTaskCommand:
    def execute(self, context: ImageDownloadContext) -> ImageDownloadContext:
        ensure_media_directories()
        if not context.remote_url or not self._is_downloadable_url(context.remote_url):
            return context

        file_name = self._build_file_name(context.remote_url, context.word_id, context.word)
        local_path = IMAGE_MEDIA_DIR / file_name
        if local_path.exists() and local_path.stat().st_size > 0:
            context.local_path = local_path
            context.local_url = media_url("images", file_name)
            self._persist(context)
            return context

        request = Request(
            context.remote_url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
                )
            },
        )

        with urlopen(request, timeout=30) as response:
            local_path.write_bytes(response.read())

        context.local_path = local_path
        context.local_url = media_url("images", file_name)
        self._persist(context)
        return context

    def _is_downloadable_url(self, remote_url: str) -> bool:
        return remote_url.startswith("http://") or remote_url.startswith("https://")

    def _build_file_name(self, remote_url: str, word_id: int, word: str) -> str:
        parsed_url = urlparse(remote_url)
        suffix = Path(parsed_url.path).suffix.lower()

        if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".gif", ".svg"}:
            suffix = ".jpg"

        if suffix == ".svg":
            return f"{slugify(f'{word_id}-{word}')}.svg"

        return f"{slugify(f'{word_id}-{word}')}{suffix}"

    def _persist(self, context: ImageDownloadContext) -> None:
        session = SessionLocal()
        try:
            row = session.query(VocabularyModel).filter(VocabularyModel.id == context.word_id).first()
            if row is not None:
                row.local_url = context.local_url
                row.image_url = context.local_url or context.remote_url
                session.commit()
        finally:
            session.close()


def download_image_task(word_id: int, word: str, remote_url: str) -> ImageDownloadContext:
    return DownloadImageTaskCommand().execute(
        ImageDownloadContext(word_id=word_id, word=word, remote_url=remote_url)
    )
