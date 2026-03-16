from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Paths
    data_dir: Path = BASE_DIR / "data"
    raw_dir: Path = BASE_DIR / "data" / "raw"
    chunks_dir: Path = BASE_DIR / "data" / "chunks"
    indexes_dir: Path = BASE_DIR / "data" / "indexes"

    # chunking
    chunk_size: int = 512
    chunk_overlap: int = 50

    # embeddings
    embedding_model: str = "BAAI/bge-small-en-v1.5"

    # retreival
    retrieval_top_k: int = 20
    rerank_top_k: int = 5
    no_answer_threshold: float = 0.3

    # LLM
    ollama_model: str = "llama3.2"
    ollama_base_url: str = "http://localhost:11434"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    log_level: str = "INFO"


settings = Settings()
