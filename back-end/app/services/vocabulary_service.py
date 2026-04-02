from app.patterns.factory.factory_provider import FactoryProvider

factory_provider = FactoryProvider()


def get_vocabulary_by_topic(topic: str) -> dict:
    factory = factory_provider.get_factory(topic)
    vocabulary_list = factory.get_vocabulary_topic()
    return {"vocabulary": [vocab.__dict__ for vocab in vocabulary_list]}