from research_pulse.config import Settings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class PdfChunker:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )

    def chunk(self, pages: list[dict]) -> list[dict]:
        try:
            chunks = []
            for page in pages:
                chunk_strings = self.splitter.split_text(page["text"])
                for chunk_index, chunk_text in enumerate(chunk_strings):
                    chunk_data = {
                        "chunk_id": f"{page['tenant_id']}__{page['source_file']}__page{page['page_number']}__chunk{chunk_index}",
                        "text": chunk_text,
                        "chunk_index": chunk_index,
                        "tenant_id": page["tenant_id"],
                        "source_file": page["source_file"],
                        "page_number": page["page_number"],
                        "title": page["title"],
                        "author": page["author"],
                    }

                    chunks.append(chunk_data)
                return chunks
        except Exception as e:
            raise RuntimeError(f"Failed to chunk pages: {e}") from e
