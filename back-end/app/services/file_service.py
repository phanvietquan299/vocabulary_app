from app.patterns.TemplateMethod.CSVVocabularyImporter import CSVVocabularyImporter
from app.patterns.TemplateMethod.JSONVocabularyImporter import JSONVocabularyImporter

def import_csv_file_vocabulary(file):
    importer = CSVVocabularyImporter()
    importer.import_file_process(file)

def import_json_file_vocabulary(file):
    importer = JSONVocabularyImporter()
    importer.import_file_process(file)