from app.core.database import SessionLocal
from app.core.media import ensure_media_directories
from app.models.vocabulary_model import VocabularyModel
from app.patterns.bridge.media_bridge import DictionaryApiAudioProvider, PexelsImageProvider, VocabularyMedia
from app.patterns.factory.factory_provider import FactoryProvider

factory_provider = FactoryProvider()
media_bridge = VocabularyMedia(PexelsImageProvider(), DictionaryApiAudioProvider())


def generate_vocabulary_media(word_id: str, session_id: str | None = None) -> dict:
    word = factory_provider.get_vocabulary_by_id(word_id)
    if not word:
        raise ValueError(f"Word with id '{word_id}' not found.")

    ensure_media_directories()
    asset = media_bridge.build(word)

    session = SessionLocal()
    try:
        row = session.query(VocabularyModel).filter(VocabularyModel.id == word.id).first()
        if row is not None:
            row.image_url = asset.image.url
            row.audio_url = asset.audio.url if asset.audio else row.audio_url
            session.commit()
    finally:
        session.close()

    return {
        "word_id": word.id,
        "word": word.word,
        "meaning": word.meaning,
        "image_url": asset.image.url,
        "audio_url": asset.audio.url if asset.audio else None,
    }
