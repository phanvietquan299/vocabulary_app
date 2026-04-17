from app.patterns.observer.IObserver import Observer
from app.core.websocket import push_learned_words_to_session


class ObserverLearnedProcess(Observer):

    async def update(self, session_id: str, learned_words: list[dict]):
        print("[ObserverLearnedProcess] Updating session with learned words:", [word['word'] for word in learned_words])
        await push_learned_words_to_session(session_id, learned_words)
        
