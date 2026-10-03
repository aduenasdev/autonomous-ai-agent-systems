import json, os
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'past_cases.json')

class LTM_Retriever:
    def __init__(self):
        os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
        if not os.path.exists(DATA_PATH):
            # create sample cases
            sample = [
                {"id":"c1","title":"Gateway timeout ERR504", "text":"Users see ERR504 when upstream service times out", "resolution":"Restart upstream service; check network"},
                {"id":"c2","title":"High CPU spike", "text":"CPU usage > 90% when batch job runs", "resolution":"Scale workers; optimize job"},
                {"id":"c3","title":"Database connection errors", "text":"DB connection timeouts and increased latency", "resolution":"Check DB pool; increase connections"}
            ]
            with open(DATA_PATH,'w') as f:
                json.dump(sample, f, indent=2)
        with open(DATA_PATH) as f:
            self.cases = json.load(f)

    def find_similar(self, text, topk=3):
        text_l = text.lower()
        scores = []
        for c in self.cases:
            # simple similarity by keyword overlap
            common = 0
            for w in c['text'].lower().split():
                if w in text_l:
                    common += 1
            scores.append((common, c))
        scores.sort(reverse=True, key=lambda x: x[0])
        return [c for sc,c in scores[:topk] if sc>0]
