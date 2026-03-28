from app.models.topic import Topic
from app.models.vocabulary import Vocabulary
from app.patterns.factory.animal_factory import AnimalFactory
from app.patterns.factory.factory_provider import FactoryProvider
from app.patterns.factory.family_factory import FamilyFactory
from app.patterns.factory.school_factory import SchoolFactory
from app.patterns.factory.travel_factory import TravelFactory
from app.patterns.factory.work_factory import WorkFactory

'''
Fake classes for testing factory pattern
docker compose exec backend python -m pytest tests/test_factory_pattern.py -q
'''

class FakeWord:
    def __init__(self, word, meaning, topic, pronunciation=None, image_url=None):
        self.word = word
        self.meaning = meaning
        self.topic = topic
        self.pronunciation = pronunciation
        self.image_url = image_url


class FakeQuery:
    def __init__(self, items):
        self.items = items

    def filter(self, *_args, **_kwargs):
        return self

    def all(self):
        return self.items


class FakeSession:
    def __init__(self, items):
        self.items = items

    def query(self, _model):
        return FakeQuery(self.items)


def test_create_vocabulary_sets_animal_topic():
    vocabulary = AnimalFactory().create_vocabulary("cat", "con meo", "/kat/", "cat.png")

    assert isinstance(vocabulary, Vocabulary)
    assert vocabulary.word == "cat"
    assert vocabulary.meaning == "con meo"
    assert vocabulary.pronunciation == "/kat/"
    assert vocabulary.image_url == "cat.png"
    assert vocabulary.topic == Topic.ANIMAL


def test_factory_provider_returns_expected_factory():
    assert isinstance(FactoryProvider.get_factory(Topic.ANIMAL), AnimalFactory)
    assert isinstance(FactoryProvider.get_factory(Topic.TRAVEL), TravelFactory)
    assert isinstance(FactoryProvider.get_factory(Topic.FAMILY), FamilyFactory)
    assert isinstance(FactoryProvider.get_factory(Topic.SCHOOL), SchoolFactory)
    assert isinstance(FactoryProvider.get_factory(Topic.WORK), WorkFactory)


def test_factory_provider_raises_for_invalid_topic():
    try:
        FactoryProvider.get_factory(Topic.FOOD)
        assert False, "Expected ValueError for unsupported topic"
    except ValueError as exc:
        assert str(exc) == "Invalid topic"


def test_animal_factory_get_vocabulary_topic_returns_vocabulary_objects():
    factory = AnimalFactory()
    factory.db = FakeSession(
        [
            FakeWord("cat", "con meo", Topic.ANIMAL.value, "/kat/", "cat.png"),
            FakeWord("dog", "con cho", Topic.ANIMAL.value, "/dog/", "dog.png"),
        ]
    )

    words = factory.get_vocabulary_topic()

    assert len(words) == 2
    assert all(isinstance(word, Vocabulary) for word in words)
    assert all(word.topic == Topic.ANIMAL for word in words)
    assert {word.word for word in words} == {"cat", "dog"}


def test_work_factory_get_vocabulary_topic_returns_work_words():
    factory = WorkFactory()
    factory.db = FakeSession(
        [
            FakeWord("office", "van phong", Topic.WORK.value),
            FakeWord("meeting", "cuoc hop", Topic.WORK.value),
        ]
    )

    words = factory.get_vocabulary_topic()

    assert len(words) == 2
    assert all(word.topic == Topic.WORK for word in words)
    assert {word.word for word in words} == {"office", "meeting"}
