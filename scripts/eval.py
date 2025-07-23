#!/usr/bin/env python3
"""
quick golden-set evaluation.
Reads tests/gold.json and prints hit-rate & faithfulness.
tests/gold.json format:
[
  {"question": "...", "answer_contains": "creatinine"},
  ...
]
"""
import json, re
from pathlib import Path
from src.rag_chain import qa_chain

GOLD_PATH = Path("tests/gold.json")

def evaluate():
    if not GOLD_PATH.exists():
        print("Create tests/gold.json first")
        return

    gold = json.loads(GOLD_PATH.read_text())
    hits = 0
    faithful = 0

    for g in gold:
        q = g["question"]
        expected = g["answer_contains"].lower()
        res = qa_chain({"query": q})
        ans = res["result"].lower()

        # basic hit-rate
        hits += int(expected in ans)

        # basic faithfulness: must cite at least one source
        srcs = res.get("source_documents", [])
        faithful += int(len(srcs) > 0)

    n = len(gold)
    print(f"Golden-set size: {n}")
    print(f"Hit-rate      : {hits/n:.2%}")
    print(f"Faithfulness  : {faithful/n:.2%}")

if __name__ == "__main__":
    evaluate()