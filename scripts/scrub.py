#!/usr/bin/env python3
"""
quick & dirty PII scrubbing for demo purposes.
Input : data/raw/*.pdf
Output: data/scrubbed/<same-name>.pdf (text-only, rebuilt)
Requires: spaCy model `en_core_web_sm`
Usage:
    python scripts/scrub.py
"""
import os, shutil, uuid
from pathlib import Path
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import spacy

RAW_DIR     = Path("data/raw")
SCRUB_DIR   = Path("data/scrubbed")
SCRUB_DIR.mkdir(exist_ok=True)

# load spaCy + Presidio
nlp = spacy.load("en_core_web_sm")
analyzer   = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def scrub_text(text: str) -> str:
    """Return text with PII replaced by <ENTITY_TYPE>."""
    results = analyzer.analyze(text=text, language="en")
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized.text

def main():
    if not RAW_DIR.exists() or not any(RAW_DIR.glob("*.pdf")):
        print("No PDFs in data/raw/")
        return

    for pdf_path in RAW_DIR.glob("*.pdf"):
        # For demo we simply copy & scrub the extracted text
        # (real apps would use pdf-lib or similar to redact boxes)
        with open(pdf_path, "rb") as f:
            text = f.read(200_000).decode(errors="ignore")  # cheap extraction
        clean = scrub_text(text)
        out_file = SCRUB_DIR / pdf_path.name
        # save as plain text for simplicity
        out_file.with_suffix(".txt").write_text(clean)
        print(f"Scrubbed {pdf_path.name}")

if __name__ == "__main__":
    main()