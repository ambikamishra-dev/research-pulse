from research_pulse.config import Settings
from research_pulse.ingestion.chunk_store import ChunkStore
from research_pulse.indexing.embedder import Embedding
from research_pulse.indexing.store import EmbedStore


class IndexingPipeline:
    def __init__(self, tenant_id: str, settings: Settings) -> None:
        self.settings = settings
        self.tenant_id = tenant_id
        self.chunk_store = ChunkStore(settings=self.settings)
        self.embedder = Embedding(settings=self.settings)
        self.embed_store = EmbedStore(settings=self.settings)

    def run(self, source_file: str) -> int:
        try:
            chunks = self.chunk_store.load(self.tenant_id, source_file)
            texts = [chunk["text"] for chunk in chunks]
            embeddings = self.embedder.embed(texts)
            self.embed_store.build(embeddings, chunks)
            return len(chunks)
        except Exception as e:
            raise RuntimeError(
                f"Could not get the length of chunks: {e}") from e
