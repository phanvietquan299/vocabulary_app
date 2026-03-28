from abc import ABC, abstractmethod

class VocabularyFactory(ABC):

    @abstractmethod
    def create_vocabulary(self, word, meaning, pronunciation=None, image_url=None):
        pass

    @abstractmethod
    def get_vocabulary_topic(self):
        pass