import datetime

from app.patterns.singleton.LearningProgressManager import LearningProgressManager
from app.patterns.factory.factory_provider import FactoryProvider

async def add_learned_word(session_id: str, word_id: str):
    manager = LearningProgressManager()
    try:
        word = FactoryProvider().get_vocabulary_by_id(word_id)
    except Exception as e:
        raise RuntimeError("Failed to load word data.") from e

    if not word:
        raise ValueError(f"Word with id '{word_id}' not found.")

    word.learn_at = datetime.datetime.now(datetime.timezone.utc)

    try:
        return await manager.mark_learned(session_id, word)
    except Exception as e:
        raise RuntimeError("Failed to save learned word progress.") from e
    
async def remove_learned_word(session_id: str, word_id: str):
    manager = LearningProgressManager()
    try:
        await manager.remove_learned(session_id, word_id)
        return {"message": f"Word with id '{word_id}' removed from learned progress for session '{session_id}'."}
    except ValueError:
        raise
    except Exception as e:
        raise RuntimeError("Failed to remove learned word progress.") from e

async def reset_learned_progress(session_id: str):
    manager = LearningProgressManager()
    try:
        manager.reset_progress(session_id)
        return {"message": f"Learning progress reset for session '{session_id}'."}
    except Exception as e:
        raise RuntimeError("Failed to reset learning progress.") from e

async def get_learned_words(session_id: str):
    manager = LearningProgressManager()
    try:
        words = manager.get_words(session_id)
        return {
            "session_id": session_id,
            "learned_words": [word.to_dict() for word in words],
        }
    except Exception as e:
        raise RuntimeError("Failed to fetch learned words.") from e
    
async def get_learned_by_topic(session_id: str, topic: str):
    manager = LearningProgressManager()
    try:
        all_learned = manager.get_words(session_id)
        learned_by_topic = [word.to_dict() for word in all_learned if word.topic == topic]
        return {
            "session_id": session_id,
            "topic": topic,
            "learned_words": learned_by_topic,
        }
    except Exception as e:
        raise RuntimeError("Failed to fetch learned words by topic.") from e

async def check_all_learned():
    instance = LearningProgressManager()
    return instance.progress_by_session
