from app.patterns.factory.factory_provider import FactoryProvider
from app.services.image_service import get_vocabulary_image

factory_provider = FactoryProvider()


def get_vocabulary_by_topic(topic: str) -> dict:
    factory = factory_provider.get_factory(topic)
    vocabulary_list = factory.get_vocabulary_topic()
    for vocab in vocabulary_list:
        try:
            media = get_vocabulary_image(str(vocab.id), refresh=True)
            vocab.local_url = media.get("local_url") or vocab.local_url
            vocab.remote_url = media.get("remote_url") or vocab.remote_url
            vocab.image_url = media.get("image_url") or vocab.local_url or vocab.remote_url or vocab.image_url
            vocab.audio_url = media.get("audio_url") or vocab.audio_url
        except Exception:
            continue
    return {"vocabulary": [vocab.__dict__ for vocab in vocabulary_list]}