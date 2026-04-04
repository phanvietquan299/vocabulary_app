from abc import ABC, abstractmethod


class Observer(ABC):
    @abstractmethod
    async def update(self, session_id: str, learned_words: list[dict]):
        pass
