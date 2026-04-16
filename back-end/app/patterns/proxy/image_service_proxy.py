from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from app.core.database import SessionLocal
from app.core.media import IMAGE_MEDIA_DIR, ensure_media_directories, media_url, word_media_stem
from app.models.vocabulary_model import VocabularyModel
from app.patterns.adapter.pexels_adapter import PexelsAdapter, StandardImage
from app.services.pexels_image_service import fetch_vocabulary_image_from_pexels


PLACEHOLDER_IMAGE_PATH = "/static/images/noir-manga-placeholder.svg"


def _is_placeholder_image_url(image_url: str | None) -> bool:
    return bool(image_url and image_url.endswith(PLACEHOLDER_IMAGE_PATH))


@dataclass
class ImageFetchResult:
    standard_image: StandardImage
    local_path: Path | None = None
    was_downloaded: bool = False


class ImageSource(ABC):
    @abstractmethod
    def fetch(self, word) -> ImageFetchResult:
        raise NotImplementedError


class PexelsImageSource(ImageSource):
    def __init__(self, api_key: str | None = None, adapter: PexelsAdapter | None = None):
        self.api_key = api_key
        self.adapter = adapter or PexelsAdapter()

    def fetch(self, word) -> ImageFetchResult:
        ensure_media_directories()
        topic_value = getattr(getattr(word, "topic", None), "value", getattr(word, "topic", None))
        image_asset = fetch_vocabulary_image_from_pexels(
            word.word,
            topic=topic_value,
            meaning=getattr(word, "meaning", None),
            api_key=self.api_key,
        )

        if image_asset.is_placeholder:
            return self._fallback_remote_image(word, word_media_stem(word), image_asset.image_url)

        standard_image = self.adapter.to_standard_image(
            {
                "id": word.id,
                "photographer": image_asset.photographer,
                "photographer_url": image_asset.photographer_url,
                "url": image_asset.source_url,
                "alt": image_asset.alt,
                "src": {
                    "original": image_asset.original_url,
                    "large2x": image_asset.image_url,
                    "large": image_asset.image_url,
                    "medium": image_asset.image_url,
                },
            }
        )

        return ImageFetchResult(
            standard_image=StandardImage(
                id=standard_image.id,
                remote_url=image_asset.image_url,
                local_url=None,
                width=standard_image.width,
                height=standard_image.height,
                alt=standard_image.alt,
                photographer=standard_image.photographer,
                source_url=standard_image.source_url,
            ),
            local_path=None,
            was_downloaded=False,
        )

    def _fallback_remote_image(self, word, stem: str, placeholder_url: str | None = None) -> ImageFetchResult:
        resolved_placeholder = placeholder_url or media_url("images", f"{stem}.svg")
        return ImageFetchResult(
            standard_image=StandardImage(
                id=stem,
                remote_url=resolved_placeholder,
                local_url=None,
                alt=getattr(word, "word", "Vocabulary image"),
                source_url=None,
            ),
            local_path=None,
            was_downloaded=False,
        )


class ImageProxy(ImageSource):
    def __init__(self, real_source: ImageSource | None = None):
        self.real_source = real_source or PexelsImageSource()

    def fetch(self, word) -> ImageFetchResult:
        ensure_media_directories()
        session = SessionLocal()
        try:
            row = session.query(VocabularyModel).filter(VocabularyModel.id == word.id).first()
            if row and row.local_url:
                local_name = Path(row.local_url).name
                local_path = IMAGE_MEDIA_DIR / local_name
                if local_path.exists() and local_path.stat().st_size > 0 and not _is_placeholder_image_url(row.local_url):
                    return ImageFetchResult(
                        standard_image=StandardImage(
                            id=str(word.id),
                            remote_url=row.remote_url or row.local_url,
                            local_url=row.local_url,
                            alt=getattr(word, "word", "Vocabulary image"),
                            source_url=row.remote_url,
                        ),
                        local_path=local_path,
                        was_downloaded=True,
                    )

            if row and row.remote_url and not _is_placeholder_image_url(row.remote_url):
                return ImageFetchResult(
                    standard_image=StandardImage(
                        id=str(word.id),
                        remote_url=row.remote_url,
                        local_url=None,
                        alt=getattr(word, "word", "Vocabulary image"),
                        source_url=row.remote_url,
                    ),
                    local_path=None,
                    was_downloaded=False,
                )

            result = self.real_source.fetch(word)
            if row is not None:
                row.remote_url = result.standard_image.remote_url
                row.image_url = result.standard_image.local_url or result.standard_image.remote_url
                session.commit()
            return result
        finally:
            session.close()