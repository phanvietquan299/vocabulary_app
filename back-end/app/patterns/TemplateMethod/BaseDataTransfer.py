from app.core.database import SessionLocal
from abc import ABC, abstractmethod
from app.patterns.repository.VocabularyRepository import VocabularyRepository

class BaseDataTransfer(ABC):
    def __init__(self):
        # self.db = SessionLocal()
        self.REQUIRED_FIELDS = [
            "word",
            "meaning",
            "pronunciation",
            # "example",
            # "local_url",
            # "remote_url",
            # "image_url",
            # "audio_url",
            "topic"
        ]
    
    def import_file_process(self, file):
        data = self.read_file(file)
        valid_data = self.validate_data(data)
        mapped_data = self.map_data(valid_data)
        self.save_data(mapped_data)

    @abstractmethod
    def read_file(self, file):
        pass

    @abstractmethod
    def validate_data(self, data):
        pass

    @abstractmethod
    def map_data(self, valid_data_list):
        pass

    def save_data(self, mapped_data_list):
        VocabularyRepository().add_list_vocabulary(mapped_data_list)
        return mapped_data_list