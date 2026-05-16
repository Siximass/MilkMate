import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


EMBED_MODEL = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


class RAGEngine:
    def __init__(self, kb_path: str):
        self.model = SentenceTransformer(EMBED_MODEL)
        self.chunks = self._load_and_chunk(kb_path)
        self.index, self.embeddings = self._build_index()

    def _load_and_chunk(self, path: str) -> list[str]:
        """Load และ Chunk ข้อมูลร้าน"""
        with open(path, encoding="utf-8") as file:
            text = file.read()

        return [chunk.strip() for chunk in text.split("\n\n") if chunk.strip()]

    def _build_index(self):
        """Embed และสร้าง vector index"""
        embeddings = self.model.encode(self.chunks, show_progress_bar=False)
        embeddings = np.array(embeddings, dtype="float32")

        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)

        return index, embeddings

    def search(self, query: str, top_k: int = 3) -> list[str]:
        """Search หา chunk ที่เกี่ยวข้องกับคำถาม"""
        query_embedding = self.model.encode([query])
        query_embedding = np.array(query_embedding, dtype="float32")

        _, indices = self.index.search(query_embedding, top_k)

        return [self.chunks[index] for index in indices[0]]