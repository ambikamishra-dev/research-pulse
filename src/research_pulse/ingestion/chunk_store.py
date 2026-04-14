from research_pulse.config import Settings
import json
from pathlib import Path


class ChunkStore:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.chunks_dir = settings.chunks_dir

    def save(self, chunks: list[dict], source_file: str) -> None:
        try:
            tenant_id = chunks[0]["tenant_id"]
            output_dir = self.chunks_dir / tenant_id
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"{Path(source_file).stem}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(chunks, f, indent=2, ensure_ascii=False)
        except Exception as e:
            raise RuntimeError(f"Failed to save chunks: {e}") from e

    def load(self, tenant_id: str, source_file: str) -> list[dict]:
        try:
            load_path = self.chunks_dir / tenant_id / \
                f"{Path(source_file).stem}.json"
            with open(load_path, 'r') as f:
                return json.load(f)

        except Exception as e:
            raise RuntimeError(f"Failed to load chunks: {e}") from e
