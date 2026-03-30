import uuid

from app.patterns.singleton.LearningProgressManager import LearningProgressManager

'''
Fake classes for testing singleton pattern
docker compose exec backend python -m pytest tests/test_singleton.py -q
'''


def test_learning_progress_separates_multiple_sessions():
    manager = LearningProgressManager()

    session_id_1 = str(uuid.uuid4())
    session_id_2 = str(uuid.uuid4())

    manager.reset_progress(session_id_1)
    manager.reset_progress(session_id_2)

    manager.mark_learned(session_id_1, "cat")
    manager.mark_learned(session_id_1, "dog")
    manager.mark_learned(session_id_1, "cat") # Duplicate

    manager.mark_learned(session_id_2, "plane")
    manager.mark_learned(session_id_2, "train")
    manager.mark_learned(session_id_2, "train") # Duplicate

    assert manager.count(session_id_1) == 2
    assert manager.count(session_id_2) == 2

    assert manager.get_words(session_id_1) == {"cat", "dog"}
    assert manager.get_words(session_id_2) == {"plane", "train"}

    assert "plane" not in manager.get_words(session_id_1)
    assert "cat" not in manager.get_words(session_id_2)
