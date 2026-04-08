import fitz
from pathlib import Path
from research_pulse.config import Settings


class PDFLoader:
    def __init__(self, tenant_id: str, settings: Settings):
        self.tenant_id = tenant_id
        self.settings = settings

    def load(self, pdf_path: Path) -> list[dict]:
        try:
            with fitz.open(pdf_path) as doc:
                title = doc.metadata.get("title", "Unknown Title")
                author = doc.metadata.get("author", "Unknown Author")
                pages = []
                for page in doc:
                    text = page.get_text()
                    if not text.strip():
                        continue

                    page_data = {
                        "text": text,
                        "page_number": page.number+1,
                        "source_file": pdf_path.name,
                        "tenant_id": self.tenant_id,
                        "title": title,
                        "author": author
                    }
                    pages.append(page_data)
                return pages
        except Exception as e:
            raise RuntimeError(
                f"Failed to load PDF {pdf_path.name}: {e}") from e
