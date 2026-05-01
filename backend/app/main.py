from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import chat


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Auto-ingest documents. Always in prod, only if empty in dev."""
    try:
        from app.services.rag import get_chroma_client, COLLECTION_NAME
        from app.scripts.ingest import ingest
        client = get_chroma_client()

        if settings.chroma_mode == "embedded":
            # Prod: always re-ingest to ensure fresh data after deploy
            print("Production mode — running document ingestion...")
            ingest()
            print("Ingestion complete.")
        else:
            # Dev: only ingest if collection is missing or empty
            collections = [c.name for c in client.list_collections()]
            if COLLECTION_NAME not in collections or client.get_collection(COLLECTION_NAME).count() == 0:
                print("Collection empty — running auto-ingestion...")
                ingest()
                print("Auto-ingestion complete.")
            else:
                collection = client.get_collection(COLLECTION_NAME)
                print(f"Collection '{COLLECTION_NAME}' ready ({collection.count()} chunks).")
    except Exception as e:
        print(f"Auto-ingestion failed: {e}")

    # Pre-generate CV PDFs
    try:
        from app.services.cv_pdf import generate_cv_pdf
        print("Generating CV PDFs...")
        generate_cv_pdf("en")
        generate_cv_pdf("fr")
        print("CV PDFs ready.")
    except Exception as e:
        print(f"CV PDF generation failed: {e}")
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
