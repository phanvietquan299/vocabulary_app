from app.patterns.factory.vocabulary_factory import VocabularyFactory
from app.models.vocabulary import Vocabulary
from app.models.topic import Topic
from app.core.database import SessionLocal
from app.models.vocabulary_model import VocabularyModel

class SchoolFactory(VocabularyFactory):
    db = SessionLocal()

    def create_vocabulary(self, word, meaning, pronunciation=None, image_url=None):
        return Vocabulary(word, meaning, Topic.SCHOOL, pronunciation, image_url)
    
    def get_vocabulary_topic(self):
        words = self.db.query(VocabularyModel).filter(VocabularyModel.topic == Topic.SCHOOL.value).all()
        return [Vocabulary(word.word, word.meaning, Topic.SCHOOL, word.pronunciation , word.image_url) for word in words]
