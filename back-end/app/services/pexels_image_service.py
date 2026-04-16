from __future__ import annotations

from dataclasses import dataclass
import json
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from sqlalchemy import text
from sqlalchemy.exc import OperationalError

from app.core.config import settings
from app.core.database import SessionLocal
from app.core.media import media_url
from app.patterns.adapter.pexels_adapter import PexelsAdapter


DEFAULT_STYLE_KEYWORDS = ("minimalist", "white background", "black and white", "noir")
PLACEHOLDER_FILENAME = "noir-manga-placeholder.svg"


def build_pexels_query(word: str, extra_keywords: tuple[str, ...] = DEFAULT_STYLE_KEYWORDS) -> str:
    parts = [word.strip(), *extra_keywords]
    return " ".join(part for part in parts if part)


def build_pexels_query_candidates(
    word: str,
    topic: str | None = None,
    topic_keywords: tuple[str, ...] = (),
    meaning: str | None = None,
    extra_keywords: tuple[str, ...] = DEFAULT_STYLE_KEYWORDS,
) -> list[str]:
    normalized_word = (word or "").strip()
    normalized_topic = (topic or "").strip().lower()
    meaning_tokens = tuple(token for token in (meaning or "").replace("/", " ").split() if token)

    candidates: list[str] = []

    if normalized_word:
        semantic_parts = [normalized_word, *topic_keywords, *meaning_tokens]
        candidates.append(" ".join(semantic_parts).strip())

    if normalized_word and topic_keywords:
        candidates.append(build_pexels_query(f"{normalized_word} {' '.join(topic_keywords)}", extra_keywords))

    if topic_keywords:
        candidates.append(" ".join(topic_keywords))

    if meaning:
        candidates.append(build_pexels_query(f"{normalized_word} {meaning.strip()}", extra_keywords))

    if normalized_word and normalized_topic:
        candidates.append(f"{normalized_word} {normalized_topic}")

    if normalized_word:
        candidates.append(build_pexels_query(normalized_word, extra_keywords))

    if normalized_word and topic_keywords:
        candidates.append(build_pexels_query(f"{normalized_word} {' '.join(topic_keywords)}", extra_keywords))

    if topic_keywords:
        candidates.append(build_pexels_query(" ".join(topic_keywords), extra_keywords))

    unique_candidates: list[str] = []
    seen: set[str] = set()
    for candidate in candidates:
        normalized_candidate = " ".join(candidate.split())
        if normalized_candidate and normalized_candidate not in seen:
            seen.add(normalized_candidate)
            unique_candidates.append(normalized_candidate)

    return unique_candidates


def _normalize_topic_keywords(raw_keywords: str | None) -> tuple[str, ...]:
    if not raw_keywords:
        return ()

    keywords: list[str] = []
    for chunk in raw_keywords.replace(";", ",").replace("|", ",").split(","):
        normalized_chunk = " ".join(chunk.strip().split())
        if normalized_chunk:
            keywords.append(normalized_chunk)

    return tuple(keywords)


def _get_topic_query_keywords(topic: str | None) -> tuple[str, ...]:
    normalized_topic = (topic or "").strip().lower()
    if not normalized_topic:
        return ()

    session = SessionLocal()
    try:
        row = session.execute(
            text("SELECT keywords FROM topic_image_configs WHERE topic = :topic"),
            {"topic": normalized_topic},
        ).scalar_one_or_none()
        configured_keywords = _normalize_topic_keywords(row)
        if configured_keywords:
            return configured_keywords
    except OperationalError:
        pass
    finally:
        session.close()

    return tuple(token for token in normalized_topic.replace("-", " ").split() if token)


@dataclass(frozen=True)
class VocabularyImageAsset:
    word: str
    query: str
    image_url: str
    original_url: str
    photographer: str | None
    photographer_url: str | None
    source_url: str | None
    alt: str
    is_placeholder: bool = False

    def to_dict(self) -> dict:
        return {
            "word": self.word,

            "query": self.query,
            "image_url": self.image_url,
            "original_url": self.original_url,
            "photographer": self.photographer,
            "photographer_url": self.photographer_url,
            "source_url": self.source_url,
            "alt": self.alt,
            "is_placeholder": self.is_placeholder,
            "credit": self.build_credit_text(),
        }

    def build_credit_text(self) -> str:
        if self.is_placeholder:
            return "Fallback Manga placeholder"
        if self.photographer and self.photographer_url:
            return f"Photo by {self.photographer} on Pexels"
        if self.photographer:
            return f"Photo by {self.photographer} on Pexels"
        return "Photo from Pexels"


class NullVocabularyImage:
    def __init__(self, word: str, query: str):
        self.word = word
        self.query = query

    def to_asset(self) -> VocabularyImageAsset:
        placeholder_url = media_url("images", PLACEHOLDER_FILENAME)
        return VocabularyImageAsset(
            word=self.word,
            query=self.query,
            image_url=placeholder_url,
            original_url=placeholder_url,
            photographer="Copilot placeholder",
            photographer_url=None,
            source_url=None,
            alt=f"{self.word} manga placeholder",
            is_placeholder=True,
        )


class PexelsImageAdapterService:
    def __init__(self, adapter: PexelsAdapter | None = None):
        self.adapter = adapter or PexelsAdapter()

    def to_asset(
        self,
        payload: dict,
        word: str,
        query: str,
        focus_keywords: tuple[str, ...] | None = None,
    ) -> VocabularyImageAsset:
        photos = payload.get("photos") or []
        if not photos:
            return NullVocabularyImage(word, query).to_asset()

        first_photo = self._select_best_photo(photos, word, focus_keywords or ())
        standard_image = self.adapter.to_standard_image(first_photo)
        if not standard_image.remote_url:
            return NullVocabularyImage(word, query).to_asset()

        best_image_url = (
            first_photo.get("src", {}).get("original")
            or first_photo.get("src", {}).get("large2x")
            or first_photo.get("src", {}).get("large")
            or standard_image.remote_url
        )

        return VocabularyImageAsset(
            word=word,
            query=query,
            image_url=best_image_url,
            original_url=first_photo.get("src", {}).get("original") or standard_image.remote_url,
            photographer=first_photo.get("photographer"),
            photographer_url=first_photo.get("photographer_url"),
            source_url=standard_image.source_url,
            alt=standard_image.alt or f"{word} illustration",
            is_placeholder=False,
        )

    def _select_best_photo(self, photos: list[dict], word: str, focus_keywords: tuple[str, ...]) -> dict:
        fallback_photo = photos[0]
        if not focus_keywords:
            return fallback_photo

        best_photo = fallback_photo
        best_score = -1
        normalized_word = word.lower()

        for photo in photos:
            alt_text = f"{photo.get('alt', '')} {photo.get('photographer', '')}".lower()
            score = 0

            if normalized_word and normalized_word in alt_text:
                score += 5

            for keyword in focus_keywords:
                if keyword and keyword.lower() in alt_text:
                    score += 3

            if any(token in alt_text for token in ("student", "study", "classroom", "desk", "books", "passport", "suitcase", "luggage", "road", "travel", "family", "parent", "mother", "father", "home", "office", "work", "meeting", "food", "meal", "plate", "kitchen", "animal", "pet")):
                score += 1

            if score > best_score:
                best_score = score
                best_photo = photo

        return best_photo


def _request_pexels_payload(query: str, api_key: str) -> dict:
    base_url = settings.pexels_api_base_url.rstrip("/")
    request_url = f"{base_url}/search?{urlencode({'query': query, 'per_page': 5, 'orientation': 'portrait'})}"
    request = Request(
        request_url,
        headers={
            "Authorization": api_key,
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
            ),
            "Referer": "https://www.pexels.com/",
        },
    )

    with urlopen(request, timeout=25) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_vocabulary_image_from_pexels(
    word: str,
    topic: str | None = None,
    meaning: str | None = None,
    api_key: str | None = None,
    extra_keywords: tuple[str, ...] = DEFAULT_STYLE_KEYWORDS,
) -> VocabularyImageAsset:
    normalized_word = (word or "").strip()
    normalized_topic = (topic or "").strip().lower() or None
    topic_keywords = _get_topic_query_keywords(normalized_topic)
    focus_keywords = topic_keywords
    query_candidates = build_pexels_query_candidates(
        normalized_word,
        topic=normalized_topic,
        topic_keywords=topic_keywords,
        meaning=meaning,
        extra_keywords=extra_keywords,
    )
    query = query_candidates[0] if query_candidates else build_pexels_query(normalized_word, extra_keywords)

    if not normalized_word:
        return NullVocabularyImage("vocabulary", query).to_asset()

    effective_api_key = api_key or settings.pexels_api_key
    if not effective_api_key:
        return NullVocabularyImage(normalized_word, query).to_asset()

    adapter_service = PexelsImageAdapterService()
    last_error: Exception | None = None

    for candidate_query in query_candidates or [query]:
        try:
            payload = _request_pexels_payload(candidate_query, effective_api_key)
        except (HTTPError, URLError, OSError, json.JSONDecodeError) as exc:
            last_error = exc
            continue

        asset = adapter_service.to_asset(payload, normalized_word, candidate_query, focus_keywords=focus_keywords)
        if not asset.is_placeholder:
            return asset

        last_error = None

    if last_error is not None:
        return NullVocabularyImage(normalized_word, query).to_asset()

    return NullVocabularyImage(normalized_word, query).to_asset()