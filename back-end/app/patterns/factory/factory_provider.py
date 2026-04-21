# import from folder of Dockerfile
from app.patterns.factory.animal_factory import AnimalFactory
from app.patterns.factory.travel_factory import TravelFactory
from app.patterns.factory.family_factory import FamilyFactory
from app.patterns.factory.school_factory import SchoolFactory
from app.patterns.factory.work_factory import WorkFactory
from app.patterns.factory.music_factory import MusicFactory
from app.models.topic import Topic

from app.models.vocabulary_model import VocabularyModel
from app.core.database import SessionLocal
from app.models.vocabulary import Vocabulary
from app.patterns.repository.VocabularyRepository import VocabularyRepository

class FactoryProvider:

    factories = {
        Topic.ANIMAL: AnimalFactory(),
        Topic.TRAVEL: TravelFactory(),
        Topic.FAMILY: FamilyFactory(),
        Topic.SCHOOL: SchoolFactory(),
        Topic.WORK: WorkFactory(),
        Topic.MUSIC: MusicFactory(),
    }
    # db = SessionLocal()

    @classmethod
    def get_factory(cls, topic):
        if topic not in cls.factories:
            raise ValueError("Invalid topic")
        print("[FactoryProvider] Providing factory for topic:", topic)
        return cls.factories[topic]
       
    def get_all_vocabulary(self):
        return VocabularyRepository().get_all_vocabulary()

    def get_all_vocabulary_items(self):
        return [
            Vocabulary(
                id=word_model.id,
                word=word_model.word,
                meaning=word_model.meaning,
                topic=Topic(word_model.topic),
                pronunciation=word_model.pronunciation,
                local_url=word_model.local_url,
                remote_url=word_model.remote_url,
                image_url=word_model.image_url,
                audio_url=word_model.audio_url,
            )
            for word_model in self.get_all_vocabulary()
        ]

    def get_vocabulary_by_id(self, word_id: str):
        try:
            word_model = VocabularyRepository().get_vocabulary_by_id(word_id)
            if not word_model:
                return None
            return Vocabulary(
                id=word_model.id,
                word=word_model.word,
                meaning=word_model.meaning,
                topic=Topic(word_model.topic),
                pronunciation=word_model.pronunciation,
                local_url=word_model.local_url,
                remote_url=word_model.remote_url,
                image_url=word_model.image_url,
                audio_url=word_model.audio_url,
            )
        except Exception as e:
            print("[FactoryProvider] Error fetching vocabulary by ID:", str(e))
            raise e
