class Vocabulary:
    def __init__(self, word, meaning, topic, pronunciation=None, image_url=None):
        self.word = word
        self.meaning = meaning
        self.pronunciation = pronunciation
        self.image_url = image_url
        self.topic = topic

    def to_dict(self):
        return {
            "word": self.word,
            "meaning": self.meaning,
            "pronunciation": self.pronunciation,
            "image_url": self.image_url,
            "topic": self.topic.value
        }
