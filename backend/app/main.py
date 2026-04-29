from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Auto-ingest documents if ChromaDB collection is empty."""
    try:
        from app.services.rag import get_chroma_client, COLLECTION_NAME
        client = get_chroma_client()
        collections = [c.name for c in client.list_collections()]
        if COLLECTION_NAME not in collections:
            print("Collection not found — running auto-ingestion...")
            from app.scripts.ingest import ingest
            ingest()
            print("Auto-ingestion complete.")
        else:
            collection = client.get_collection(COLLECTION_NAME)
            if collection.count() == 0:
                print("Collection empty — running auto-ingestion...")
                from app.scripts.ingest import ingest
                ingest()
                print("Auto-ingestion complete.")
            else:
                print(f"Collection '{COLLECTION_NAME}' ready ({collection.count()} chunks).")
    except Exception as e:
        print(f"Auto-ingestion skipped: {e}")
    yield


app = FastAPI(title="asknarymane API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat.router)
