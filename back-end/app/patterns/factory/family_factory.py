from app.patterns.factory.vocabulary_factory import VocabularyFactory
from app.models.vocabulary import Vocabulary
from app.core.database import SessionLocal
from app.models.vocabulary_model import VocabularyModel
from app.models.topic import Topic

class FamilyFactory(VocabularyFactory):
    db = SessionLocal()

    def create_vocabulary(self, word, meaning, pronunciation=None, image_url=None):
        return Vocabulary(word, meaning, Topic.FAMILY, pronunciation, image_url)

    def get_vocabulary_topic(self):
        words = self.db.query(VocabularyModel).filter(VocabularyModel.topic == Topic.FAMILY.value).all()
        return [Vocabulary(word.word, word.meaning, Topic.FAMILY, word.pronunciation , word.image_url) for word in words]