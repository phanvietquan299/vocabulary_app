from app.patterns.factory.factory_provider import FactoryProvider
from app.patterns.singleton.LearningProgressManager import LearningProgressManager

async def get_dashboard_by_user(session_id: str):
    
    # Process all words
    all_word = len(FactoryProvider().get_all_vocabulary())
    learned_word = len(LearningProgressManager().get_learned_progress(session_id))
    
    # Process by topic
    topics = FactoryProvider().factories
    topic_progress = {
        topic: {
            "total": len(FactoryProvider().get_factory(topic).get_vocabulary_topic()),
            "learned": len(set(FactoryProvider().get_factory(topic).get_vocabulary_topic()) & LearningProgressManager().get_learned_progress(session_id))
        }
        for topic in topics
    }
    
    return {
        "overall_progress": {
            "total": all_word,
            "learned": learned_word,
            "percentage": (learned_word / all_word * 100) if all_word > 0 else 0
        },
        "topic_progress": topic_progress
    }

