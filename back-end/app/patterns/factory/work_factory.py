from app.patterns.factory.vocabulary_factory import VocabularyFactory
from app.models.vocabulary import Vocabulary
from app.models.topic import Topic
from app.core.database import SessionLocal
from app.models.vocabulary_model import VocabularyModel

class WorkFactory(VocabularyFactory):
    def __init__(self):
        self.db = SessionLocal()

    def create_vocabulary(self, word, meaning, pronunciation=None, image_url=None):
        return Vocabulary(word, meaning, Topic.WORK, pronunciation, image_url)
    
    def get_vocabulary_topic(self):
        words = self.db.query(VocabularyModel).filter(VocabularyModel.topic == Topic.WORK.value).all()
        return [
            Vocabulary(
                id=word.id,
                word=word.word,
                meaning=word.meaning,
                topic=Topic.WORK,
                pronunciation=word.pronunciation,
                image_url=word.image_url,
            )
            for word in words
        ]
