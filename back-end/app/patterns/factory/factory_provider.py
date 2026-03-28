# import from folder of Dockerfile
from app.patterns.factory.animal_factory import AnimalFactory
from app.patterns.factory.travel_factory import TravelFactory
from app.patterns.factory.family_factory import FamilyFactory
from app.patterns.factory.school_factory import SchoolFactory
from app.patterns.factory.work_factory import WorkFactory
from app.models.topic import Topic

class FactoryProvider:

    factories = {
        Topic.ANIMAL: AnimalFactory(),
        Topic.TRAVEL: TravelFactory(),
        Topic.FAMILY: FamilyFactory(),
        Topic.SCHOOL: SchoolFactory(),
        Topic.WORK: WorkFactory()
    }

    @classmethod
    def get_factory(cls, topic):
        if topic not in cls.factories:
            raise ValueError("Invalid topic")
        return cls.factories[topic]