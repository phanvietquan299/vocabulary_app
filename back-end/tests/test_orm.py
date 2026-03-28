from app.core.database import SessionLocal
from app.models.vocabulary_model import VocabularyModel

def query_orm():
    db = SessionLocal()
    words = db.query(VocabularyModel).all()
    db.close()
    print([word.to_dict() for word in words])
    return words

def test_orm():
    words = query_orm()
    assert isinstance(words, list)