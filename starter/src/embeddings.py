import os
from typing import Protocol
from sentence_transformers import SentenceTransformer

class Embedder(Protocol):
    model_name: str
    dimensions: int

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        ...

    def embed_query(self, question: str) -> list[float]:
        ...

class LocalSentenceTransformerEmbedder:
    """Real local embedding implementation satisfying Embedder protocol."""

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2") -> None:
        self.model_name = model_name
        self.model = SentenceTransformer(model_name, local_files_only=True)
        self.dimensions = self.model.get_sentence_embedding_dimension()

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts)
        return embeddings.tolist()

    def embed_query(self, question: str) -> list[float]:
        embeddings = self.model.encode([question])
        return embeddings[0].tolist()
