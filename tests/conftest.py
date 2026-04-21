import pytest
from pathlib import Path
from research_pulse.config import settings
from research_pulse.ingestion.loader import PDFLoader
from research_pulse.ingestion.chunker import PdfChunker
from research_pulse.ingestion.chunk_store import ChunkStore
from research_pulse.indexing.embedder import Embedding

TEST_PDF = Path("data/raw/deep_learning_nature.pdf")
TEST_TENANT = "wiu_cs"


@pytest.fixture(scope="session")
def test_pdf():
    return TEST_PDF


@pytest.fixture(scope="session")
def tenant_id():
    return TEST_TENANT


@pytest.fixture(scope="session")
def pages():
    loader = PDFLoader(tenant_id=TEST_TENANT, settings=settings)
    return loader.load(TEST_PDF)


@pytest.fixture(scope="session")
def chunks(pages):
    chunker = PdfChunker(settings=settings)
    return chunker.chunk(pages)


@pytest.fixture(scope="session")
def embedder():
    return Embedding(settings=settings)


@pytest.fixture(scope="session")
def embeddings(embedder, chunks):
    texts = [chunk["text"]for chunk in chunks]
    return embedder.embed(texts)
