from research_pulse.config import Settings
from pathlib import Path
import faiss
import numpy as np
import json


class EmbedStore:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.indexes_dir = settings.indexes_dir
        self.dimension = settings.embedding_dimension

    def build(self, embeddings: np.ndarray, chunks: list[dict]) -> None:
        try:
            tenant_id = chunks[0]["tenant_id"]
            index = faiss.IndexFlatL2(self.dimension)
            embeddings = embeddings.astype(np.float32)
            index.add(embeddings)
            output_dir = self.indexes_dir / tenant_id
            output_dir.mkdir(parents=True, exist_ok=True)
            faiss.write_index(index, str(output_dir / "index.faiss"))
            chunks_path = output_dir / "chunks.json"
            with open(chunks_path, "w", encoding="utf-8") as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Failed to index: {e}") from e

    def load(self, tenant_id: str) -> tuple[faiss.Index, list[dict]]:
        try:
            index_path = self.indexes_dir / tenant_id / "index.faiss"
            chunks_path = self.indexes_dir / tenant_id / "chunks.json"
            if not index_path.exists():
                raise FileNotFoundError(
                    f"No FAISS index for tenant '{tenant_id}'. Run indexing pipeline first.")
            if not chunks_path.exists():
                raise FileNotFoundError(
                    f"No chunks file for tenant '{tenant_id}'. Run indexing pipeline first.")
            index = faiss.read_index(str(index_path))
            with open(chunks_path, 'r', encoding="utf-8") as f:
                chunks = json.load(f)
            return index, chunks

        except Exception as e:
            raise RuntimeError(
                f"Failed to load index for {tenant_id}: {e}") from e
