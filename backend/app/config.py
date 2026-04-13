from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral"
    api_host: str = "0.0.0.0"
    api_port: int = 8080
    chroma_host: str = "localhost"
    chroma_port: int = 8000
    documents_dir: str = "documents"
    frontend_url: str = "http://localhost:3000"
    cors_origins: list[str] = ["http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
