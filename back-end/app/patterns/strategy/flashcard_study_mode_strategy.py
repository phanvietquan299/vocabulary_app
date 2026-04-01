from app.patterns.strategy.study_mode_strategy import StudyModeStrategy
from app.models.vocabulary import Vocabulary

class FlashcardStudyModeStrategy(StudyModeStrategy):
    def build_exam_object(self, word: Vocabulary) -> dict:
        return word.to_dict()
