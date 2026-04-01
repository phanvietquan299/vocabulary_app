# import from folder of Dockerfile
from app.patterns.factory.animal_factory import AnimalFactory
from app.patterns.factory.travel_factory import TravelFactory
from app.patterns.factory.family_factory import FamilyFactory
from app.patterns.factory.school_factory import SchoolFactory
from app.patterns.factory.work_factory import WorkFactory
from app.models.topic import Topic

from app.models.vocabulary_model import VocabularyModel
from app.core.database import SessionLocal
from app.models.vocabulary import Vocabulary

class FactoryProvider:

    factories = {
        Topic.ANIMAL: AnimalFactory(),
        Topic.TRAVEL: TravelFactory(),
        Topic.FAMILY: FamilyFactory(),
        Topic.SCHOOL: SchoolFactory(),
        Topic.WORK: WorkFactory()
    }
    db = SessionLocal()

    @classmethod
    def get_factory(cls, topic):
        if topic not in cls.factories:
            raise ValueError("Invalid topic")
        return cls.factories[topic]
       
    def get_all_vocabulary(self):
        return self.db.query(VocabularyModel).all()

    def get_all_vocabulary_items(self):
        return [
            Vocabulary(
                id=word_model.id,
                word=word_model.word,
                meaning=word_model.meaning,
                topic=Topic(word_model.topic),
                pronunciation=word_model.pronunciation,
                image_url=word_model.image_url,
            )
            for word_model in self.get_all_vocabulary()
        ]

    def get_vocabulary_by_id(self, word_id: str):
        word_model = self.db.query(VocabularyModel).filter(VocabularyModel.id == word_id).first()
        if not word_model:
            return None
        return Vocabulary(
            id=word_model.id,
            word=word_model.word,
            meaning=word_model.meaning,
            topic=Topic(word_model.topic),
            pronunciation=word_model.pronunciation,
            image_url=word_model.image_url,
        )
