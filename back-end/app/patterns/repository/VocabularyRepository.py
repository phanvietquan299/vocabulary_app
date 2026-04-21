from app.core.database import SessionLocal
from app.models.vocabulary_model import VocabularyModel

class VocabularyRepository:
    def __init__(self):
        self.db = SessionLocal()
    
    def get_vocabulary_by_topic(self, topic):
        print("[VocabularyRepository] Fetching vocabulary for topic:", topic)
        works = self.db.query(VocabularyModel).filter(VocabularyModel.topic == topic.value).all()
        self.db.close()
        return works
    
    def add_list_vocabulary(self, vocab_data):
        try:
            print("[VocabularyRepository] Adding new vocabulary:")
            vocabulary_list = [VocabularyModel(**data) for data in vocab_data]
            self.db.add_all(vocabulary_list)
            self.db.commit()
            self.db.close()
            print("[VocabularyRepository] Successfully added vocabulary.")
        except Exception as e:
            self.db.rollback()
            self.db.close()
            print("[VocabularyRepository] Error adding vocabulary:", str(e))
            raise e
        
    def get_vocabulary_by_id(self, word_id):
        try:
            print("[VocabularyRepository] Fetching vocabulary with ID:", word_id)
            vocab = self.db.query(VocabularyModel).filter(VocabularyModel.id == word_id).first()
            self.db.close()
            return vocab
        except Exception as e:
            self.db.close()
            print("[VocabularyRepository] Error fetching vocabulary:", str(e))
            raise e
        
    def get_all_vocabulary(self):
        try:
            print("[VocabularyRepository] Fetching all vocabulary.")
            vocab_list = self.db.query(VocabularyModel).all()
            self.db.close()
            return vocab_list
        except Exception as e:
            self.db.close()
            print("[VocabularyRepository] Error fetching all vocabulary:", str(e))
            raise e
