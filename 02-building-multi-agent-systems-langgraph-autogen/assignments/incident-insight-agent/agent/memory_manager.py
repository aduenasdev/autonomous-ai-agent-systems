import time
class MemoryManager:
    def __init__(self):
        # store last N events' titles for quick matching
        self.store = []
        self.maxlen = 50

    def add(self, event_id, event):
        self.store.append({'id': event_id, 'title': event.get('title'), 'time': time.time()})
        if len(self.store) > self.maxlen:
            self.store.pop(0)

    def count_similar(self, title):
        # naive substring match count for simplicity
        title_low = (title or '').lower()
        return sum(1 for e in self.store if title_low in (e.get('title') or '').lower())
