import time


class MemoryManager:
    def __init__(self):
        self.history = []

    def add(self, item: dict) -> None:
        item_copy = dict(item)
        item_copy['_ts'] = time.time()
        self.history.append(item_copy)

    def last(self, n: int = 5) -> list[dict]:
        return self.history[-n:]

    def all(self) -> list[dict]:
        return self.history

    def user_messages(self) -> list[str]:
        return [item['user'] for item in self.history if 'user' in item]

    def clear(self) -> None:
        self.history.clear()
