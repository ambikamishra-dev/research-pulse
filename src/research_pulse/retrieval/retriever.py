import numpy as np
import faiss
from research_pulse.config import Settings
from research_pulse.indexing.embedder import Embedding
from research_pulse.indexing.store import EmbedStore


class Retriever:
    def __init__(self, tenant_id: str, settings: Settings):
        self.settings = settings
        self.embedder = Embedding(settings=settings)
        embed_store = EmbedStore(settings=settings)
        self.index, self.chunks = embed_store.load(tenant_id)
        self.tenant_id = tenant_id

    def search(self, query: str) -> list[dict]:
        try:

            embedded_query = self.embedder.embed([query])
            embedded_query = embedded_query.reshape(1, 384)
            embedded_query = embedded_query.astype(np.float32)
            distances, indices = self.index.search(embedded_query, k=20)

            results = []
            for idx, distance in zip(indices[0], distances[0]):
                if idx == -1:
                    continue
                chunk = self.chunks[idx].copy()
                chunk["score"] = float(distance)
                results.append(chunk)
            return results
        except Exception as e:
            raise RuntimeError(
                f"Could not get the index and distance of query: {e}") from e
