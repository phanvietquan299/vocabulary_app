from app.patterns.factory.vocabulary_factory import VocabularyFactory
from app.models.vocabulary import Vocabulary
from app.models.topic import Topic
from app.core.database import SessionLocal
from app.models.vocabulary_model import VocabularyModel

class TravelFactory(VocabularyFactory):
    db = SessionLocal()

    def create_vocabulary(self, word, meaning, pronunciation=None, image_url=None):
        return Vocabulary(word, meaning, Topic.TRAVEL, pronunciation, image_url)
    
    def get_vocabulary_topic(self):
        words = self.db.query(VocabularyModel).filter(VocabularyModel.topic == Topic.TRAVEL.value).all()
        return [Vocabulary(word.word, word.meaning, Topic.TRAVEL, word.pronunciation , word.image_url) for word in words]
        
