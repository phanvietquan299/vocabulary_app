import datetime

class Vocabulary:
    def __init__(
        self,
        word: str,
        meaning: str,
        topic,
        pronunciation=None,
        local_url=None,
        remote_url=None,
        image_url=None,
        audio_url=None,
        id=None,
    ):
        self.id = id
        self.word: str = word
        self.meaning: str = meaning
        self.pronunciation: str = pronunciation
        self.local_url: str = local_url
        self.remote_url: str = remote_url
        self.image_url: str = image_url
        self.audio_url: str = audio_url
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
        learn_at = self.learn_at

        if learn_at and learn_at.tzinfo is None:
            learn_at = learn_at.replace(tzinfo=datetime.timezone.utc)

        return {
            "id": self.id,
            "word": self.word,
            "meaning": self.meaning,
            "pronunciation": self.pronunciation,
            "local_url": self.local_url,
            "remote_url": self.remote_url,
            "image_url": self.image_url,
            "audio_url": self.audio_url,
            "topic": self.topic.value,
            "learn_at": learn_at.isoformat() if learn_at else None
        }
