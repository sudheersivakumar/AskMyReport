"""
Gradio chat UI
Usage:
    python -m src.app
"""
import gradio as gr
from src.rag_chain import qa_chain

def chat(query):
    res = qa_chain({"query": query})
    answer = res["result"]
    sources = "\n".join({d.metadata["source"] for d in res["source_documents"]})
    return answer, sources

iface = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(label="Question", placeholder="Ask anything about the reports…"),
    outputs=[
        gr.Textbox(label="Answer"),
        gr.Textbox(label="Sources")
    ],
    title="AskMyReport – Medical RAG Chatbot ",
    theme="soft"
)

if __name__ == "__main__":
    iface.launch(server_name="127.0.0.1", server_port=7860)