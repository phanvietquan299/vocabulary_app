from enum import Enum

class Topic(str, Enum):
    ANIMAL = "animal"
    TRAVEL = "travel"
    FAMILY = "family"
    SCHOOL = "school"
    WORK = "work"
    FOOD = "food"