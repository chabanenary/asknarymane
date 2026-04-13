import os

# Set test environment variables before importing app
os.environ["LLM_PROVIDER"] = "ollama"
os.environ["CHROMA_HOST"] = "localhost"
os.environ["CHROMA_PORT"] = "8000"
os.environ["GROQ_API_KEY"] = "test_key"
