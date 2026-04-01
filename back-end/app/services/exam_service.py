from app.patterns.strategy.study_mode_context import StudyModeContext
from app.patterns.strategy.multiple_choice_study_mode_strategy import (
    MultipleChoiceStudyModeStrategy,
)
from app.patterns.strategy.flashcard_study_mode_strategy import (
    FlashcardStudyModeStrategy,
)
from app.patterns.strategy.SR_mode_strategy import SRModeStrategy
from app.patterns.factory.factory_provider import FactoryProvider


def get_exam_multiple_choices(word_id: str):
    factory = FactoryProvider()
    word = factory.get_vocabulary_by_id(word_id)
    if not word:
        raise ValueError(f"Word with id '{word_id}' not found.")

    all_words = factory.get_all_vocabulary_items()
    multiple_choices_strategy = StudyModeContext(
        MultipleChoiceStudyModeStrategy(all_words)
    )
    return multiple_choices_strategy.build_exam_object(word)


def get_exam_flashcard(word_id: str):
    word = FactoryProvider().get_vocabulary_by_id(word_id)
    if not word:
        raise ValueError(f"Word with id '{word_id}' not found.")

    flashcard_strategy = StudyModeContext(FlashcardStudyModeStrategy())
    return flashcard_strategy.build_exam_object(word)


def get_exam_sr(session_id: str):
    sr_strategy = SRModeStrategy(session_id)
    learned_list = sr_strategy.get_learned_sr_list()

    if not learned_list:
        raise ValueError(f"No learned words found for session '{session_id}'.")

    return {
        "session_id": session_id,
        "review_word_ids": learned_list,
        "total": len(learned_list),
    }
