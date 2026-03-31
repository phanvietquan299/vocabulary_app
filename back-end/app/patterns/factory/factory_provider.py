# import from folder of Dockerfile
from app.patterns.factory.animal_factory import AnimalFactory
from app.patterns.factory.travel_factory import TravelFactory
from app.patterns.factory.family_factory import FamilyFactory
from app.patterns.factory.school_factory import SchoolFactory
from app.patterns.factory.work_factory import WorkFactory
from app.models.topic import Topic

from app.models.vocabulary_model import VocabularyModel
from app.core.database import SessionLocal

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

    def get_vocabulary_by_word(self, word: str):
        return self.db.query(VocabularyModel).filter(VocabularyModel.word == word).first()
