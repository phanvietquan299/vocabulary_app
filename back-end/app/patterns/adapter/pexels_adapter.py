from dataclasses import dataclass


@dataclass
class StandardImage:
    id: str
    remote_url: str
    local_url: str | None = None
    width: int | None = None
    height: int | None = None
    alt: str | None = None
    photographer: str | None = None
    source_url: str | None = None


class PexelsAdapter:
    def to_standard_image(self, payload: dict) -> StandardImage:
        source = payload.get("src", {})
        return StandardImage(
            id=str(payload.get("id", "pexels-image")),
            remote_url=source.get("large2x") or source.get("large") or source.get("original") or source.get("medium") or "",
            width=payload.get("width"),
            height=payload.get("height"),
            alt=payload.get("alt") or payload.get("photographer") or "Vocabulary image",
            photographer=payload.get("photographer"),
            source_url=payload.get("url"),
        )