"""
Usage:
    python -m src.embed
"""
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from pathlib import Path
from src.chunk import chunk_docs

DB_PATH = Path("db")

def build_db():
    chunks = chunk_docs()
    texts = [c["chunk"] for c in chunks]
    metas = [{"uid": c["uid"], "source": c["source"]} for c in chunks]

    embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma.from_texts(
        texts=texts,
        metadatas=metas,
        embedding=embeddings,
        persist_directory=str(DB_PATH)
    )
    db.persist()
    print(f"Vector DB saved to {DB_PATH.resolve()}")

if __name__ == "__main__":
    build_db()