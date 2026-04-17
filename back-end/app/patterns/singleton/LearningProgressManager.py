import datetime

from app.models.vocabulary import Vocabulary
from app.patterns.observer.ObserverLearnedProcess import ObserverLearnedProcess


class LearningProgressManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.progress_by_session = {}
            cls._instance.observers = [ObserverLearnedProcess()]
        return cls._instance

    def attach_observer(self, observer):
        self.observers.append(observer)

    async def notify_observers(self, session_id: str):
        learned_word = self.progress_by_session.get(session_id, set())
        learned_words = [word.to_dict() for word in learned_word]

        for obs in self.observers:
            await obs.update(session_id, learned_words)

    async def mark_learned(self, session_id: str, word: Vocabulary):
        word.learn_at = word.learn_at or datetime.datetime.now(datetime.timezone.utc)
        if session_id not in self.progress_by_session:
            self.progress_by_session[session_id] = set()

        self.progress_by_session[session_id].add(word)
        await self.notify_observers(session_id)
        print(f"[LearningProgressManager] Marked word '{word.word}' as learned for session '{session_id}'. Total learned: {len(self.progress_by_session[session_id])}")
        return (
            f"Da danh dau tu '{word.to_dict().get('word', 'Unknown')}' "
            f"la da hoc cho session_id '{session_id}'"
        )

    async def remove_learned(self, session_id: str, word_id: str):
        if session_id in self.progress_by_session:
            words = self.progress_by_session[session_id]
            word_to_remove = None
            for word in words:
                if str(word.id) == str(word_id):
                    word_to_remove = word
                    break
            if word_to_remove:
                words.remove(word_to_remove)
                await self.notify_observers(session_id)
                return (
                    f"Da xoa tu '{word_to_remove.to_dict().get('word', 'Unknown')}' "
                    f"khoi tien trinh da hoc cho session_id '{session_id}'"
                )
            raise ValueError(
                f"Word with id '{word_id}' not found in learned progress for session '{session_id}'."
            )
        raise ValueError(f"No learning progress found for session '{session_id}'.")

    def count(self, session_id: str):
        return len(self.progress_by_session.get(session_id, set()))

    def get_words(self, session_id: str):
        return set(self.progress_by_session.get(session_id, set()))

    def reset_progress(self, session_id: str):
        if session_id in self.progress_by_session:
            del self.progress_by_session[session_id]

    def get_learned_progress(self, session_id: str):
        return self.progress_by_session.get(session_id, set())
