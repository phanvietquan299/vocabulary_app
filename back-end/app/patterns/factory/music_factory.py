from app.patterns.factory.vocabulary_factory import VocabularyFactory
from app.models.vocabulary import Vocabulary
from app.models.topic import Topic
from app.core.database import SessionLocal
from app.models.vocabulary_model import VocabularyModel
from app.patterns.repository.VocabularyRepository import VocabularyRepository


class MusicFactory(VocabularyFactory):
    def __init__(self):
        self.repository = VocabularyRepository()

    def create_vocabulary(self, word, meaning, pronunciation=None, local_url=None, remote_url=None, image_url=None, audio_url=None):
        return Vocabulary(word, meaning, Topic.MUSIC, pronunciation, local_url, remote_url, image_url, audio_url)

    def get_vocabulary_topic(self):
        words = self.repository.get_vocabulary_by_topic(Topic.MUSIC)
        return [
            Vocabulary(
                id=word.id,
                word=word.word,
                meaning=word.meaning,
                topic=Topic.MUSIC,
                pronunciation=word.pronunciation,
                local_url=word.local_url,
                remote_url=word.remote_url,
                image_url=word.image_url,
                audio_url=word.audio_url,
            )
            for word in words
        ]