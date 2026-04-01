from abc import ABC, abstractmethod
from app.models.vocabulary import Vocabulary

class StudyModeStrategy(ABC):
    @abstractmethod
    def build_exam_object(self, word: Vocabulary) -> dict:
        raise NotImplementedError
