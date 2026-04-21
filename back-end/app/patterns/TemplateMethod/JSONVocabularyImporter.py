from app.patterns.TemplateMethod.BaseDataTransfer import BaseDataTransfer
import json

class JSONVocabularyImporter(BaseDataTransfer):
    def __init__(self):
        super().__init__()

    def read_file(self, file):
        data = json.load(file.file)
        return data

    def validate_data(self, data):
        if not isinstance(data, list):
            raise ValueError("JSON data must be a list of vocabulary entries.")
        
        for entry in data:
            missing_fields = set(self.REQUIRED_FIELDS) - set(entry.keys())
            if missing_fields:
                raise ValueError(f"Missing required fields in entry: {missing_fields}")
        
        return data

    def map_data(self, valid_data_list):
        mapped_data = []
        for entry in valid_data_list:
            vocab_entry = {
                "word": entry["word"],
                "meaning": entry["meaning"],
                "pronunciation": entry.get("pronunciation", ""),
                "example": entry.get("example", ""),
                "local_url": entry.get("local_url", ""),
                "remote_url": entry.get("remote_url", ""),
                "image_url": entry.get("image_url", ""),
                "audio_url": entry.get("audio_url", ""),
                "topic": entry["topic"]
            }
            mapped_data.append(vocab_entry)
        return mapped_data