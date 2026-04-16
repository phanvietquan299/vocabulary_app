from sqlalchemy import Column, Integer, String
from app.core.database import Base

# This class creates the VocabularyModel table in the database and defines its structure.
# Provides ORM mapping for the VocabularyModel
class VocabularyModel(Base):
    __tablename__ = "vocabularies"

    id = Column(Integer, primary_key=True, index=True)
    word = Column(String(100), nullable=False)
    meaning = Column(String(255), nullable=False)
    pronunciation = Column(String(100))
    example = Column(String(255))
    local_url = Column(String(255))
    remote_url = Column(String(255))
    image_url = Column(String(255))
    audio_url = Column(String(255))
    topic = Column(String(50))

    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "meaning": self.meaning,
            "pronunciation": self.pronunciation,
            "example": self.example,
            "local_url": self.local_url,
            "remote_url": self.remote_url,
            "image_url": self.image_url,
            "audio_url": self.audio_url,
            "topic": self.topic
        }
