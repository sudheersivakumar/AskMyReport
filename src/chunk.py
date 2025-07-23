"""
Usage:
    from src.chunk import chunk_docs
Returns:
    List[dict] with keys: uid, source, chunk
"""
import json
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path

JSON_PATH = Path("data/extracted.json")

def chunk_docs(chunk_size=500, chunk_overlap=50):
    data = json.loads(JSON_PATH.read_text())
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    chunks = []
    for doc in data:
        for c in splitter.split_text(doc["text"]):
            chunks.append({
                "uid":   doc["uid"],
                "source": doc["source"],
                "chunk": c
            })
    return chunks

if __name__ == "__main__":
    cs = chunk_docs()
    print(f"Created {len(cs)} chunks")