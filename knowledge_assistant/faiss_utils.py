import faiss
import numpy as np
from .models import Chunk, Document

EMBEDDING_DIM = 384  # all-MiniLM-L6-v2 output size

class FaissIndex:
    def __init__(self):
        self.index = faiss.IndexFlatL2(EMBEDDING_DIM)
        self.chunk_ids = []  # Map index position to chunk id

    def build(self):
        chunks = Chunk.objects.all()
        if not chunks:
            return
        embeddings = []
        self.chunk_ids = []
        for chunk in chunks:
            emb = np.frombuffer(chunk.embedding, dtype=np.float32)
            if emb.shape[0] == EMBEDDING_DIM:
                embeddings.append(emb)
                self.chunk_ids.append(chunk.id)
        if embeddings:
            arr = np.stack(embeddings)
            self.index.add(arr)

    def add_chunk(self, chunk):
        emb = np.frombuffer(chunk.embedding, dtype=np.float32)
        if emb.shape[0] == EMBEDDING_DIM:
            self.index.add(emb.reshape(1, -1))
            self.chunk_ids.append(chunk.id)

    def search(self, query_emb, top_k=5):
        if self.index.ntotal == 0:
            return []
        D, I = self.index.search(query_emb.reshape(1, -1), top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.chunk_ids):
                chunk_id = self.chunk_ids[idx]
                try:
                    chunk = Chunk.objects.get(id=chunk_id)
                    results.append(chunk)
                except Chunk.DoesNotExist:
                    continue
        return results

faiss_index = FaissIndex()

def build_faiss_index():
    faiss_index.build() 