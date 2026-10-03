from collections import deque

class MemoryManager:
    def __init__(self, max_size=5):
        self.memory = deque(maxlen=max_size)

    def add(self, incident, action):
        self.memory.append({"incident": incident, "action": action})

    def get_memory(self):
        return list(self.memory)

    def clear(self):
        self.memory.clear()
