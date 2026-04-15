from sentence_transformers import SentenceTransformer
import numpy as np
from research_pulse.config import Settings


class Embedding:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.model = SentenceTransformer(settings.embedding_model)

    def embed(self, texts: list[str]) -> np.ndarray:
        try:
            embed_encode = self.model.encode(texts)
            return embed_encode
        except Exception as e:
            raise RuntimeError(f"Failed to embed: {e}") from e
