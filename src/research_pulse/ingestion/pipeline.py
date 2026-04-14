from research_pulse.config import Settings
from research_pulse.ingestion.loader import PDFLoader
from research_pulse.ingestion.chunker import PdfChunker
from research_pulse.ingestion.chunk_store import ChunkStore
from pathlib import Path


class IngestionPipeline:
    def __init__(self, tenant_id: str, settings: Settings):
        self.settings = settings
        self.tenant_id = tenant_id
        self.loader = PDFLoader(
            tenant_id=self.tenant_id, settings=self.settings)
        self.chunker = PdfChunker(settings=self.settings)
        self.store = ChunkStore(settings=self.settings)

    def run(self, pdf_path: Path) -> int:
        try:
            pages = self.loader.load(pdf_path)
            chunks = self.chunker.chunk(pages)
            self.store.save(chunks, pdf_path.name)
            return len(chunks)
        except Exception as e:
            raise RuntimeError(
                f"Failed to return number of chunks: {e}") from e
