from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # LLM provider: "ollama" or "groq"
    llm_provider: str = "ollama"

    # Ollama (local dev)
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2:1.5b"

    # Groq (cloud)
    groq_api_key: str = ""
    groq_model: str = "llama-3.3-70b-versatile"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8080

    # ChromaDB
    chroma_host: str = "localhost"
    chroma_port: int = 8000

    # GitHub
    github_username: str = "chabanenary"
    github_cache_ttl: int = 600

    # Documents
    documents_dir: str = "documents"
    documents_fr_dir: str = "documents_fr"

    # Frontend
    frontend_url: str = "http://localhost:3000"
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
