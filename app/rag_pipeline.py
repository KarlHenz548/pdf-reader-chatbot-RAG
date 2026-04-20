import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
import ollama

model = SentenceTransformer("all-MiniLM-L6-v2")

index = None
chunks = None


# Build index from uploaded PDF
def build_index(pdf_path):
    global index, chunks

    from PyPDF2 import PdfReader
    from langchain_text_splitters import RecursiveCharacterTextSplitter

    pdf = PdfReader(pdf_path)

    text = ""
    for page in pdf.pages:
        text += page.extract_text() or ""

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    embeddings = model.encode(chunks)

    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))

    print("Index built")


# Retrieve relevant chunks
def retrieve(query, k=3):
    query_emb = model.encode([query])
    D, I = index.search(np.array(query_emb), k)

    return [chunks[i] for i in I[0]]


# Generate answer
def generate_answer(query):
    context = retrieve(query)

    prompt = f"""
Use ONLY the context to answer.

Context:
{context}

Question:
{query}

If not in context, say you don't know.
"""

    response = ollama.chat(
        model="llama3",
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"]