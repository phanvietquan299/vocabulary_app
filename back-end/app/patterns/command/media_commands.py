from abc import ABC, abstractmethod
from dataclasses import dataclass
from html import escape
from pathlib import Path
from typing import Any

from app.core.database import SessionLocal
from app.core.media import IMAGE_MEDIA_DIR, ensure_media_directories, media_url, word_media_stem
from app.models.vocabulary_model import VocabularyModel


@dataclass
class VocabularyMediaContext:
    word: Any
    session_id: str | None = None
    image_path: Path | None = None
    audio_path: Path | None = None
    image_url: str | None = None
    audio_url: str | None = None


class MediaCommand(ABC):
    @abstractmethod
    async def execute(self, context: VocabularyMediaContext) -> VocabularyMediaContext:
        raise NotImplementedError


class GenerateMangaImageCommand(MediaCommand):
    async def execute(self, context: VocabularyMediaContext) -> VocabularyMediaContext:
        ensure_media_directories()
        word = context.word
        stem = word_media_stem(word)
        image_path = IMAGE_MEDIA_DIR / f"{stem}.svg"

        if not image_path.exists() or image_path.stat().st_size == 0:
            image_path.write_text(_build_manga_svg(word), encoding="utf-8")

        context.image_path = image_path
        context.image_url = media_url("images", image_path.name)
        return context


class PersistVocabularyMediaCommand(MediaCommand):
    async def execute(self, context: VocabularyMediaContext) -> VocabularyMediaContext:
        session = SessionLocal()
        try:
            row = session.query(VocabularyModel).filter(VocabularyModel.id == context.word.id).first()
            if row is not None:
                if context.image_url is not None:
                    row.image_url = context.image_url
                if context.audio_url is not None:
                    row.audio_url = context.audio_url
                session.commit()
        finally:
            session.close()

        return context


class NotifyVocabularyMediaCommand(MediaCommand):
    async def execute(self, context: VocabularyMediaContext) -> VocabularyMediaContext:
        if not context.session_id:
            return context

        from app.core.websocket import push_media_update_to_session

        await push_media_update_to_session(
            context.session_id,
            {
                "word_id": context.word.id,
                "word": context.word.word,
                "image_url": context.image_url,
                "audio_url": context.audio_url,
            },
        )
        return context


class MediaCommandInvoker:
    def __init__(self, commands: list[MediaCommand]):
        self.commands = commands

    async def run(self, context: VocabularyMediaContext) -> VocabularyMediaContext:
        current_context = context
        for command in self.commands:
            current_context = await command.execute(current_context)
        return current_context


def _build_manga_svg(word) -> str:
    title = escape(getattr(word, "word", "Vocabulary"))
    meaning = escape(getattr(word, "meaning", ""))
    pronunciation = escape(getattr(word, "pronunciation", "") or "")
    topic = escape(str(getattr(getattr(word, "topic", ""), "value", getattr(word, "topic", ""))))

    return f"""<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 960 640' role='img' aria-label='{title} manga illustration'>
  <rect width='960' height='640' fill='#ffffff'/>
  <rect x='28' y='28' width='904' height='584' rx='36' fill='none' stroke='#111111' stroke-width='10'/>
  <circle cx='185' cy='176' r='102' fill='none' stroke='#111111' stroke-width='12'/>
  <circle cx='185' cy='176' r='52' fill='none' stroke='#111111' stroke-width='10'/>
  <path d='M130 150 L75 106' stroke='#111111' stroke-width='10' stroke-linecap='round'/>
  <path d='M240 150 L295 106' stroke='#111111' stroke-width='10' stroke-linecap='round'/>
  <path d='M120 218 Q185 260 250 218' fill='none' stroke='#111111' stroke-width='10' stroke-linecap='round'/>
  <rect x='352' y='86' width='514' height='154' rx='28' fill='none' stroke='#111111' stroke-width='8'/>
  <text x='384' y='148' font-family='Arial, Helvetica, sans-serif' font-size='34' font-weight='700' fill='#111111'>{title}</text>
  <text x='384' y='186' font-family='Arial, Helvetica, sans-serif' font-size='22' fill='#333333'>{meaning}</text>
  <text x='384' y='220' font-family='Arial, Helvetica, sans-serif' font-size='18' fill='#555555'>{pronunciation}</text>
  <text x='384' y='246' font-family='Arial, Helvetica, sans-serif' font-size='14' letter-spacing='4' fill='#777777'>MANGA INK SKETCH</text>
  <g transform='translate(132 332)'>
    <rect width='696' height='198' rx='30' fill='none' stroke='#111111' stroke-width='10'/>
    <path d='M68 152 Q124 76 180 152 T292 152 T404 152 T516 152 T628 152' fill='none' stroke='#111111' stroke-width='8'/>
    <circle cx='108' cy='68' r='14' fill='#111111'/>
    <circle cx='170' cy='52' r='10' fill='#111111'/>
    <circle cx='240' cy='86' r='12' fill='#111111'/>
    <circle cx='310' cy='60' r='8' fill='#111111'/>
    <circle cx='384' cy='82' r='15' fill='#111111'/>
    <circle cx='478' cy='56' r='9' fill='#111111'/>
    <circle cx='556' cy='90' r='13' fill='#111111'/>
    <circle cx='628' cy='64' r='9' fill='#111111'/>
    <text x='44' y='172' font-family='Arial, Helvetica, sans-serif' font-size='18' fill='#444444'>topic: {topic}</text>
  </g>
</svg>"""
