'''
Do không làm login nên không có user_id để lưu tiến trình học tập
Nên sẽ dùng session_id để phân biệt tiến trình học tập của từng người dùng khác nhau
session_id sẽ được tạo ra khi người dùng bắt đầu học và sẽ được gửi kèm trong mỗi yêu cầu
session_id sẽ được tạo ngẫu nhiên ở front-end để đảm bảo tính duy nhất và bảo mật
'''
from app.patterns.observer.ObserverLearnedProcess import ObserverLearnedProcess
from app.models.vocabulary import Vocabulary

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

    # Đánh dấu (thêm từ đã học vào tiến trình của session_id)
    async def mark_learned(self, session_id: str, word: Vocabulary):
        if session_id not in self.progress_by_session:
            self.progress_by_session[session_id] = set()

        self.progress_by_session[session_id].add(word)
        await self.notify_observers(session_id)
        return f"Đã đánh dấu từ '{word.to_dict().get('word', 'Unknown')}' là đã học cho session_id '{session_id}'"
    
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
                return f"Đã xóa từ '{word_to_remove.to_dict().get('word', 'Unknown')}' khỏi tiến trình đã học cho session_id '{session_id}'"
            else:
                raise ValueError(f"Word with id '{word_id}' not found in learned progress for session '{session_id}'.")
        else:
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
