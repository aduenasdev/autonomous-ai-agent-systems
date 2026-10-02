import random, time, uuid
# Simulates incident logs of different types

INCIDENT_TEMPLATES = [
    {'title': 'Auth service high CPU and latency', 'desc': 'Auth tokens spike causing CPU usage and latency.', 'base': {'cpu': 92, 'latency_ms': 520, 'errors': 5}},
    {'title': 'API gateway timeouts', 'desc': 'Gateway reports high latency and some 502 errors under load.', 'base': {'cpu': 65, 'latency_ms': 620, 'errors': 25}},
    {'title': 'DB connection errors', 'desc': 'Database connection pool exhausted resulting in errors.', 'base': {'cpu': 55, 'latency_ms': 120, 'errors': 110}},
    {'title': 'Background job failures', 'desc': 'Async worker failing due to task timeout.', 'base': {'cpu': 40, 'latency_ms': 80, 'errors': 12}},
    {'title': 'Cache miss storm', 'desc': 'Sudden cache miss rate causing higher db load.', 'base': {'cpu': 75, 'latency_ms': 300, 'errors': 8}},
]

class LogStreamer:
    def __init__(self):
        random.seed(42)
    def next_event(self):
        tmpl = random.choice(INCIDENT_TEMPLATES)
        # add some noise
        cpu = int(tmpl['base']['cpu'] + random.randint(-5,10))
        latency = int(tmpl['base']['latency_ms'] + random.randint(-50,80))
        errors = int(tmpl['base']['errors'] + random.randint(-10,50))
        ev = {
            'id': str(uuid.uuid4()),
            'title': tmpl['title'],
            'description': tmpl['desc'],
            'metrics': {'cpu': max(0, cpu), 'latency_ms': max(0, latency), 'errors': max(0, errors)}
        }
        # tiny sleep to simulate stream timing
        time.sleep(0.01)
        return ev
