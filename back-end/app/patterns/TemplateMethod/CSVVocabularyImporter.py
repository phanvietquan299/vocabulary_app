from app.patterns.TemplateMethod.BaseDataTransfer import BaseDataTransfer

import pandas as pd

class CSVVocabularyImporter(BaseDataTransfer):
    def __init__(self):
        super().__init__()

    def read_file(self, file):
        df = pd.read_csv(file.file, encoding="utf-8-sig")

        df.columns = df.columns.str.strip().str.lower()
        df = df.fillna("")

        file.file.seek(0)
        return df

    def validate_data(self, data):
        actual_fields = set(data.columns)
        missing_fields = set(self.REQUIRED_FIELDS) - actual_fields
        if missing_fields:
            raise ValueError(f"Missing required fields: {missing_fields}")
        return data

    def map_data(self, valid_data_list):
        mapped_data = []
        for _, row in valid_data_list.iterrows():
            vocab_entry = {
                "word": row["word"],
                "meaning": row["meaning"],
                "pronunciation": row.get("pronunciation", ""),
                "example": row.get("example", ""),
                "local_url": row.get("local_url", ""),
                "remote_url": row.get("remote_url", ""),
                "image_url": row.get("image_url", ""),
                "audio_url": row.get("audio_url", ""),
                "topic": row["topic"]
            }
            mapped_data.append(vocab_entry)
        return mapped_data