import datetime

class Vocabulary:
    def __init__(
        self,
        word: str,
        meaning: str,
        topic,
        pronunciation=None,
        image_url=None,
        id=None,
    ):
        self.id = id
        self.word: str = word
        self.meaning: str = meaning
        self.pronunciation: str = pronunciation
        self.image_url: str = image_url
        self.topic: str = topic
        self.learn_at: datetime = None

    def __hash__(self):
        if self.id is not None:
            return hash(self.id)
        return hash((self.word, self.topic))

    def __eq__(self, other):
        if not isinstance(other, Vocabulary):
            return False
        if self.id is not None and other.id is not None:
            return self.id == other.id
        return self.word == other.word and self.topic == other.topic

    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "meaning": self.meaning,
            "pronunciation": self.pronunciation,
            "image_url": self.image_url,
            "topic": self.topic.value,
            "learn_at": self.learn_at.isoformat() if self.learn_at else None
        }
