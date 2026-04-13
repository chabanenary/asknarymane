"""Ingest markdown documents into ChromaDB."""

import re
from pathlib import Path

import chromadb

from app.config import settings
from app.services.embeddings import OllamaEmbeddingFunction

COLLECTION_NAME = "narymane_profile"


def read_markdown_files(base_dir: str) -> list[dict]:
    """Read all markdown files and return docs with metadata."""
    docs = []
    base = Path(base_dir)
    for md_file in sorted(base.rglob("*.md")):
        content = md_file.read_text(encoding="utf-8")
        category = md_file.parent.name if md_file.parent != base else "general"
        docs.append(
            {
                "content": content,
                "source": str(md_file.relative_to(base)),
                "category": category,
            }
        )
    return docs


def chunk_by_sections(text: str, source: str, category: str) -> list[dict]:
    """Split markdown by H1/H2 sections, keeping headers as context."""
    chunks = []
    # Extract document title (first H1)
    doc_title = ""
    title_match = re.search(r"^#\s+(.+)$", text, re.MULTILINE)
    if title_match:
        doc_title = title_match.group(1).strip()

    # Split on H2 (##) headers
    sections = re.split(r"(?=^##\s)", text, flags=re.MULTILINE)

    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Extract section header if present
        section_header = ""
        header_match = re.match(r"^##\s+(.+)$", section, re.MULTILINE)
        if header_match:
            section_header = header_match.group(1).strip()

        # Build a context-enriched chunk
        prefix = f"[{category}] {doc_title}"
        if section_header:
            prefix += f" > {section_header}"

        chunk_text = f"{prefix}\n\n{section}"

        chunks.append(
            {
                "text": chunk_text,
                "metadata": {
                    "source": source,
                    "category": category,
                    "doc_title": doc_title,
                    "section": section_header or doc_title,
                },
            }
        )

    return chunks


def ingest():
    """Main ingestion pipeline."""
    client = chromadb.HttpClient(host=settings.chroma_host, port=settings.chroma_port)

    # Reset collection if it exists
    try:
        client.delete_collection(COLLECTION_NAME)
    except Exception:
        pass

    collection = client.create_collection(
        name=COLLECTION_NAME,
        embedding_function=OllamaEmbeddingFunction(),
    )

    # Ingest both English and French documents
    sources = [
        (settings.documents_dir, "en"),
        (settings.documents_fr_dir, "fr"),
    ]

    all_chunks = []
    all_metadatas = []
    all_ids = []

    for docs_dir, lang in sources:
        docs = read_markdown_files(docs_dir)
        print(f"Found {len(docs)} documents ({lang})")
        for doc in docs:
            sections = chunk_by_sections(doc["content"], doc["source"], doc["category"])
            for i, section in enumerate(sections):
                all_chunks.append(section["text"])
                meta = section["metadata"]
                meta["lang"] = lang
                all_metadatas.append(meta)
                all_ids.append(f"{lang}_{doc['source']}_{i}")

    print(f"Ingesting {len(all_chunks)} chunks into ChromaDB...")

    batch_size = 50
    for i in range(0, len(all_chunks), batch_size):
        end = min(i + batch_size, len(all_chunks))
        collection.add(
            documents=all_chunks[i:end],
            metadatas=all_metadatas[i:end],
            ids=all_ids[i:end],
        )

    print(f"Done! {collection.count()} chunks stored in collection '{COLLECTION_NAME}'")


if __name__ == "__main__":
    ingest()
