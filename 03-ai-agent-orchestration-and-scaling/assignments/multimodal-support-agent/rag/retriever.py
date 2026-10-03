import json
from difflib import SequenceMatcher

class IncidentRetriever:
    def __init__(self, data_path="data/incidents.json"):
        with open(data_path, "r") as f:
            self.incidents = json.load(f)

    def similarity(self, a: str, b: str):
        return SequenceMatcher(None, a.lower(), b.lower()).ratio()

    def get_similar(self, new_incident: dict, threshold=0.5):
        text = new_incident["description"]
        similar = []

        for incident in self.incidents:
            score = self.similarity(text, incident["description"])
            if score > threshold:
                similar.append({**incident, "similarity": round(score, 2)})

        return similar
