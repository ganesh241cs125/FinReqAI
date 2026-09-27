from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .loader import load_documents, chunk_text
from ..config import KB_DIR

class LocalRAG:
    def __init__(self):
        self.sources = []
        self.chunks = []
        self.vectorizer = None
        self.matrix = None
        self.rebuild()

    def rebuild(self):
        self.sources = []
        self.chunks = []
        for doc in load_documents(KB_DIR):
            for chunk in chunk_text(doc["text"]):
                self.sources.append(doc["source"])
                self.chunks.append(chunk)

        if self.chunks:
            self.vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1,2))
            self.matrix = self.vectorizer.fit_transform(self.chunks)

    def search(self, query, k=4):
        if not self.chunks or self.matrix is None:
            return []
        q = self.vectorizer.transform([query])
        scores = cosine_similarity(q, self.matrix)[0]
        indices = scores.argsort()[::-1][:k]
        return [
            {
                "source": self.sources[i],
                "text": self.chunks[i],
                "score": round(float(scores[i]), 4)
            }
            for i in indices if scores[i] > 0
        ]
