from app.core.database import SessionLocal
from app.core.media import ensure_media_directories
from app.models.vocabulary_model import VocabularyModel
from app.patterns.command.image_download_commands import download_image_task
from app.patterns.factory.factory_provider import FactoryProvider
from app.patterns.proxy.image_service_proxy import ImageProxy

factory_provider = FactoryProvider()
image_proxy = ImageProxy()


def _is_downloadable_url(remote_url: str | None) -> bool:
    return bool(remote_url and (remote_url.startswith("http://") or remote_url.startswith("https://")))


def get_vocabulary_image(word_id: str, refresh: bool = True) -> dict:
    word = factory_provider.get_vocabulary_by_id(word_id)
    if not word:
        raise ValueError(f"Word with id '{word_id}' not found.")

    ensure_media_directories()
    fetched_image = image_proxy.fetch(word)

    local_url = fetched_image.standard_image.local_url
    remote_url = fetched_image.standard_image.remote_url

    if refresh and remote_url and not local_url and _is_downloadable_url(remote_url):
        downloaded = download_image_task(word.id, word.word, remote_url)
        local_url = downloaded.local_url or local_url

    session = SessionLocal()
    try:
        row = session.query(VocabularyModel).filter(VocabularyModel.id == word.id).first()
        if row is not None:
            row.remote_url = remote_url
            row.local_url = local_url
            row.image_url = local_url or remote_url
            session.commit()
    finally:
        session.close()

    return {
        "word_id": word.id,
        "word": word.word,
        "remote_url": remote_url,
        "local_url": local_url,
        "image_url": local_url or remote_url,
    }
