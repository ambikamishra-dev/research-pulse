import pytest
from pathlib import Path
from research_pulse.config import settings
from research_pulse.ingestion.chunk_store import ChunkStore
from research_pulse.ingestion.pipeline import IngestionPipeline


def test_loader_returns_valid_pages(pages):

    assert isinstance(pages, list)
    assert len(pages) > 0
    assert "text" in pages[0]
    assert "page_number" in pages[0]
    assert "tenant_id" in pages[0]


def test_chunker_produces_valid_chunks(chunks):

    assert isinstance(chunks, list)
    assert len(chunks) > 0
    for chunk in chunks:
        assert "chunk_index" in chunk
        assert "tenant_id" in chunk
        assert "chunk_id" in chunk
        assert "text" in chunk

    for chunk in chunks:
        assert len(chunk["text"].strip()) > 0

    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    assert len(chunk_ids) == len(set(chunk_ids))


def test_chunk_store_saves_and_loads(chunks, test_pdf):

    store = ChunkStore(settings=settings)
    store.save(chunks, test_pdf.name)

    expected_path = settings.chunks_dir / \
        chunks[0]["tenant_id"] / f"{test_pdf.stem}.json"
    assert expected_path.exists()

    loaded_chunks = store.load(chunks[0]["tenant_id"], test_pdf.name)

    assert isinstance(loaded_chunks, list)
    assert len(loaded_chunks) == len(chunks)
    assert loaded_chunks[0]["chunk_id"] == chunks[0]["chunk_id"]


def test_ingestion_pipeline_end_to_end(test_pdf, tenant_id):
    ingestion_pipeline = IngestionPipeline(
        tenant_id=tenant_id, settings=settings)
    count = ingestion_pipeline.run(test_pdf)

    assert count > 0

    expected_path_run = settings.chunks_dir / \
        tenant_id / f"{test_pdf.stem}.json"
    assert expected_path_run.exists()
