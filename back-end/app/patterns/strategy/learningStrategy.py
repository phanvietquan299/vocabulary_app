from typing import List
from abc import ABC, abstractmethod
from app.models.vocabulary import Vocabulary

class LearningStrategy(ABC):
    @abstractmethod
    def get_exam_object(self, word_object: Vocabulary):
        pass