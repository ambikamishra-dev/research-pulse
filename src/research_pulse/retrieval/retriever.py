import numpy as np
import faiss
from research_pulse.config import Settings
from research_pulse.indexing.embedder import Embedding
from research_pulse.indexing.store import EmbedStore


def __init__(self, tenant_id: str, settings: Settings):
    self.settings = settings
    self.embedder = Embedding(settings=settings)
    embed_store = EmbedStore(settings=settings)
    self.index, self.chunks = embed_store.load(tenant_id)
    self.tenant_id = tenant_id


def search(self, query: str) -> list[dict]:
