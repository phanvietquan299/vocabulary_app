from app.models.vocabulary import Vocabulary
from app.patterns.strategy.study_mode_strategy import StudyModeStrategy


class StudyModeContext:
    def __init__(self, strategy: StudyModeStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: StudyModeStrategy):
        self._strategy = strategy

    def build_exam_object(self, word: Vocabulary) -> dict:
        return self._strategy.build_exam_object(word)
