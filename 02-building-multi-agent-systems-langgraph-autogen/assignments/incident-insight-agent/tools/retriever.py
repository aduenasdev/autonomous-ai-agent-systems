import json, os
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

class Retriever:
    def __init__(self, path=None):
        self.path = path or os.path.join(os.path.dirname(__file__), '..', 'data', 'incidents.json')
        self.docs = []
        self.vectorizer = TfidfVectorizer(max_features=400, stop_words='english')
        self.vectors = None
        self._fit = False
        self._load()

    def _load(self):
        if not os.path.exists(self.path):
            self.docs = []
            return
        with open(self.path, 'r', encoding='utf-8') as f:
            self.docs = json.load(f)
        texts = [d.get('description','') for d in self.docs]
        if texts:
            self.vectors = self.vectorizer.fit_transform(texts).toarray()
            self._fit = True

    def query(self, q, top_k=3):
        if not self._fit:
            return []
        qv = self.vectorizer.transform([q]).toarray()[0]
        sims = self.vectors @ qv
        idx = sims.argsort()[::-1][:top_k]
        results = []
        for i in idx:
            results.append({'id': self.docs[i].get('id'), 'title': self.docs[i].get('title'), 'description': self.docs[i].get('description'), 'score': float(sims[i])})
        return results
