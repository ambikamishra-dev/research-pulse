import pytest
import numpy as np
import faiss
from research_pulse.config import settings
from research_pulse.indexing.store import EmbedStore
from research_pulse.indexing.pipeline import IndexingPipeline

EXPECTED_DIMENSION = 384


def test_embedder_produces_correct_shape(embeddings, chunks):

    assert isinstance(embeddings, np.ndarray)
    assert embeddings.shape == (len(chunks), EXPECTED_DIMENSION)


def test_embed_store_builds_and_saves_index(embeddings, chunks):
    store = EmbedStore(settings=settings)
    store.build(embeddings, chunks)

    tenant_id = chunks[0]["tenant_id"]
    index_path = settings.indexes_dir / tenant_id / "index.faiss"
    chunks_path = settings.indexes_dir / tenant_id / "chunks.json"

    assert index_path.exists()
    assert chunks_path.exists()
    assert chunks_path.stat().st_size > 0


def test_embed_store_loads_index_correctly():
    store = EmbedStore(settings=settings)
    index, chunks = store.load("wiu_cs")
    assert isinstance(index, faiss.Index)
    assert isinstance(chunks, list)
    assert len(chunks) > 0
    assert "chunk_id" in chunks[0]
