from app.patterns.singleton.LearningProgressManager import LearningProgressManager

async def add_learned_word(session_id: str, word: str):
    manager = LearningProgressManager()
    return await manager.mark_learned(session_id, word)

async def reset_learned_progress(session_id: str):
    manager = LearningProgressManager()
    manager.reset_progress(session_id)
    return {"message": f"Learning progress reset for session '{session_id}'."}

async def get_learned_words(session_id: str):
    manager = LearningProgressManager()
    words = manager.get_words(session_id)
    return {"session_id": session_id, "learned_words": list(words)}

async def check_all_learned():
    instance = LearningProgressManager()
    return instance.progress_by_session
