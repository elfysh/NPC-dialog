from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    chunks_path: Path = Path("./skyrim_chunks.jsonl")
    faiss_index_path: Path = Path("./skyrim_faiss.index")
    embedding_model_name: str = "qilowoq/bge-m3-en-ru"
    lora_path: str = "./sft_model_final"
    max_seq_length: int = 8192
    max_new_tokens_generate: int = 256
    load_in_4bit: bool = True
    conversation_logs_dir: Path = Path("./logs/conversations")
    host: str = "0.0.0.0"
    port: int = 8000


settings = Settings()
