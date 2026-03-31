class ContextStrategy:
    def __init__(self, strategy):
        self._strategy = strategy

    def get_strategy(self):
        return self._strategy()