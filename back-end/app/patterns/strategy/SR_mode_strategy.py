from app.patterns.singleton.LearningProgressManager import LearningProgressManager

class SRModeStrategy:
    def __init__(self, session_id: str):
        self.learned_sr_list = set()
        learned = LearningProgressManager().get_learned_progress(session_id)
        for word in learned:
            self.learned_sr_list.add(word.id)      

    def get_learned_sr_list(self):
        return sorted(self.learned_sr_list)
