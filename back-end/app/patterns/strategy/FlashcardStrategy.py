from app.patterns.strategy.learningStrategy import LearningStrategy
from app.models.vocabulary import Vocabulary

class FlashCardStrategy(LearningStrategy):
    def get_learned_words(self, words: list[Vocabulary]):
        return [word.to_dict() for word in words]