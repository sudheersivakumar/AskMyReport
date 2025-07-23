"""

Usage:
    python -m src.extract
Output:
    data/extracted.json
"""
import json, uuid, os, sys
import pdfplumber
from pathlib import Path

RAW_DIR   = Path("data/raw")
OUT_FILE  = Path("data/extracted.json")

def extract_all():
    docs = []
    if not RAW_DIR.exists() or not any(RAW_DIR.glob("*.pdf")):
        print("No PDFs found in data/raw/")
        sys.exit(1)

    for pdf_path in RAW_DIR.glob("*.pdf"):
        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join(p.extract_text() or "" for p in pdf.pages)
        docs.append({
            "uid": str(uuid.uuid4()),
            "source": pdf_path.name,
            "text": text
        })

    OUT_FILE.parent.mkdir(exist_ok=True)
    OUT_FILE.write_text(json.dumps(docs, indent=2, ensure_ascii=False))
    print(f"Extracted {len(docs)} documents → {OUT_FILE}")

if __name__ == "__main__":
    extract_all()