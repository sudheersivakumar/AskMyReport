"""
RetrievalQA chain using Groq + Chroma
"""
import os, sys
from pathlib import Path
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Groq LLM wrapper
from groq import Groq
from langchain.llms.base import LLM
from typing import Any, List, Optional

load_dotenv()
if not os.getenv("GROQ_API_KEY"):
    sys.exit("GROQ_API_KEY not found in .env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

class GroqLLM(LLM):
    model: str = os.getenv("GROQ_MODEL", "llama3-8b-8192")

    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        resp = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
            temperature=0,
            max_tokens=1024
        )
        return resp.choices[0].message.content

    @property
    def _identifying_params(self): return {"name": self.model}
    @property
    def _llm_type(self): return "groq"

embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = Chroma(
    persist_directory="db",
    embedding_function=embeddings
)

prompt = PromptTemplate(
    template="You are a helpful medical assistant. "
             "Use only the context below.\n\n"
             "Context: {context}\n\n"
             "Question: {question}\nAnswer:",
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=GroqLLM(),
    chain_type="stuff",
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True,
    chain_type_kwargs={"prompt": prompt}
)