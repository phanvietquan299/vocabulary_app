'''
Do không làm login nên không có user_id để lưu tiến trình học tập
Nên sẽ dùng session_id để phân biệt tiến trình học tập của từng người dùng khác nhau
session_id sẽ được tạo ra khi người dùng bắt đầu học và sẽ được gửi kèm trong mỗi yêu cầu
session_id sẽ được tạo ngẫu nhiên ở front-end để đảm bảo tính duy nhất và bảo mật
'''

class LearningProgressManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.progress_by_session = {}
        return cls._instance

    def mark_learned(self, session_id: str, word):
        if session_id not in self.progress_by_session:
            self.progress_by_session[session_id] = set()
        self.progress_by_session[session_id].add(word)

    def count(self, session_id: str):
        return len(self.progress_by_session.get(session_id, set()))
    
    def get_words(self, session_id: str):
        return set(self.progress_by_session.get(session_id, set()))


    def reset_progress(self, session_id: str):
        if session_id in self.progress_by_session:
            del self.progress_by_session[session_id]