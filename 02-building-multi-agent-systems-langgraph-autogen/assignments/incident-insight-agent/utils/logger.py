import json, time
from pathlib import Path
class AuditLogger:
    def __init__(self, source, logfile='logs/audit.log'):
        self.source = source
        self.logfile = Path(logfile)
        self.logfile.parent.mkdir(parents=True, exist_ok=True)
    def log(self, event_type, payload):
        entry = {
            'time': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
            'source': self.source,
            'event': event_type,
            'payload': payload
        }
        with self.logfile.open('a', encoding='utf-8') as f:
            f.write(json.dumps(entry) + '\n')
