from abc import ABC, abstractmethod

class VocabularyFactory(ABC):

    @abstractmethod
    def create_vocabulary(
        self,
        word,
        meaning,
        pronunciation=None,
        local_url=None,
        remote_url=None,
        image_url=None,
        audio_url=None,
    ):
        pass

    @abstractmethod
    def get_vocabulary_topic(self):
        pass