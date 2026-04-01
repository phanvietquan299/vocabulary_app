import random

from app.models.vocabulary import Vocabulary
from app.patterns.strategy.study_mode_strategy import StudyModeStrategy

class MultipleChoiceStudyModeStrategy(StudyModeStrategy):
    def __init__(self, all_words: list[Vocabulary], num_choices: int = 3):
        self._all_words = all_words
        self._num_choices = num_choices

    def _get_random_meanings(self, correct_word: Vocabulary) -> list[str]:
        wrong_words = [word for word in self._all_words if word.id != correct_word.id]
        wrong_choices = random.sample(
            wrong_words,
            min(self._num_choices - 1, len(wrong_words)),
        )

        answers = [correct_word.meaning] + [word.meaning for word in wrong_choices]
        random.shuffle(answers)
        return answers

    def build_exam_object(self, word: Vocabulary) -> dict:
        answers = self._get_random_meanings(word)
        return {
            "id": word.id,
            "word": word.word,
            "correct_answer": word.meaning,
            "answers": answers,
        }
