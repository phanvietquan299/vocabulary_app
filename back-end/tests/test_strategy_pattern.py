from app.models.topic import Topic
from app.models.vocabulary import Vocabulary
from app.patterns.singleton.LearningProgressManager import LearningProgressManager
from app.patterns.strategy.SR_mode_strategy import SRModeStrategy
from app.patterns.strategy.flashcard_study_mode_strategy import (
    FlashcardStudyModeStrategy,
)
from app.patterns.strategy.multiple_choice_study_mode_strategy import (
    MultipleChoiceStudyModeStrategy,
)
from app.patterns.strategy.study_mode_context import StudyModeContext

"""
Simple tests for strategy classes
docker compose exec backend python -m pytest tests/test_strategy_pattern.py -q
"""


def make_word(word_id, word, meaning):
    return Vocabulary(
        id=word_id,
        word=word,
        meaning=meaning,
        topic=Topic.ANIMAL,
        pronunciation=f"/{word}/",
        image_url=f"{word}.png",
    )


def test_flashcard_strategy_returns_full_word_data():
    word = make_word(1, "cat", "con meo")

    result = FlashcardStudyModeStrategy().build_exam_object(word)

    assert result["id"] == 1
    assert result["word"] == "cat"
    assert result["meaning"] == "con meo"
    assert result["topic"] == Topic.ANIMAL.value
    assert result["image_url"] == "cat.png"


def test_multiple_choice_strategy_builds_answers_with_correct_meaning():
    word = make_word(1, "cat", "con meo")
    all_words = [
        word,
        make_word(2, "dog", "con cho"),
        make_word(3, "bird", "con chim"),
    ]

    result = MultipleChoiceStudyModeStrategy(all_words).build_exam_object(word)

    assert result["id"] == 1
    assert result["word"] == "cat"
    assert result["correct_answer"] == "con meo"
    assert "con meo" in result["answers"]
    assert len(result["answers"]) == 3


def test_study_mode_context_can_switch_strategy():
    word = make_word(1, "cat", "con meo")
    all_words = [word, make_word(2, "dog", "con cho")]
    context = StudyModeContext(FlashcardStudyModeStrategy())

    flashcard_result = context.build_exam_object(word)
    context.set_strategy(MultipleChoiceStudyModeStrategy(all_words, num_choices=2))
    multiple_choice_result = context.build_exam_object(word)

    assert flashcard_result["meaning"] == "con meo"
    assert multiple_choice_result["correct_answer"] == "con meo"
    assert len(multiple_choice_result["answers"]) == 2


def test_sr_mode_strategy_returns_sorted_learned_word_ids():
    manager = LearningProgressManager()
    session_id = "strategy-test-session"
    manager.reset_progress(session_id)
    manager.progress_by_session[session_id] = {
        make_word(3, "bird", "con chim"),
        make_word(1, "cat", "con meo"),
        make_word(2, "dog", "con cho"),
    }

    result = SRModeStrategy(session_id).get_learned_sr_list()

    assert result == [1, 2, 3]
    manager.reset_progress(session_id)
