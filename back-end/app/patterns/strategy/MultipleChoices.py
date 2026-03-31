from app.patterns.strategy.learningStrategy import LearningStrategy
from app.patterns.factory.factory_provider import FactoryProvider
import random

class MultipleChoicesStrategy(LearningStrategy):
    @staticmethod
    def get_random_meanings(correct_word: str, num_choices: int = 3):
        all_words = FactoryProvider().get_all_vocabulary()
        correct_vocab = FactoryProvider().get_vocabulary_by_word(correct_word)

        if not correct_vocab:
            return []

        wrong_words = [w for w in all_words if w.word != correct_word]
        wrong_choices = random.sample(wrong_words, min(num_choices - 1, len(wrong_words)))

        answers = [correct_vocab.meaning] + [w.meaning for w in wrong_choices]
        random.shuffle(answers)
        return answers

    def get_exam_object(self, word: str):
        word_object = FactoryProvider().get_vocabulary_by_word(word)
        answers = self.get_random_meanings(word, 3)

        return {
            "word": word_object.word,
            "correct_answer": word_object.meaning,
            "answers": answers
        }
