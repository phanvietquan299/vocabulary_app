from app.patterns.strategy.ContextStrategy import ContextStrategy
from app.patterns.strategy.MultipleChoices import MultipleChoicesStrategy

def get_exam_multiple_choices(word: str):
    multiple_choices_strategy = ContextStrategy(MultipleChoicesStrategy)
    style = multiple_choices_strategy.get_strategy()
    return style.get_exam_object(word)
