"""Retrieval: top-k=5 with MMR reranking; BM25 fallback when cosine
similarity drops below threshold.

STATUS: interface-only. Backed by Qdrant (self-hosted) in production.
"""
from __future__ import annotations


class PolicyRetriever:
    def __init__(self, vector_store_client, top_k: int = 5, similarity_floor: float = 0.65):
        self.vector_store_client = vector_store_client
        self.top_k = top_k
        self.similarity_floor = similarity_floor

    def retrieve(self, query: str) -> list[dict]:
        raise NotImplementedError(
            "1. cosine similarity search -> 2. MMR rerank -> "
            "3. BM25 fallback if top score < similarity_floor"
        )
