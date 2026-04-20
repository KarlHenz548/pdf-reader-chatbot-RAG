from reportlab.pdfgen import canvas

def create_pdf():
    c = canvas.Canvas("data/sample.pdf")

    text = c.beginText(40, 750)
    text.setFont("Helvetica", 11)

    content = """
Artificial Intelligence (AI) is a field of computer science focused on building systems that can simulate human intelligence.

Machine Learning allows systems to learn from data instead of being explicitly programmed.

Deep Learning uses neural networks with many layers for complex tasks like image and speech recognition.

Retrieval-Augmented Generation (RAG) improves LLM responses by retrieving relevant documents before answering.

FAISS is a vector search library used to store and search embeddings efficiently.
"""

    for line in content.split("\n"):
        text.textLine(line)

    c.drawText(text)
    c.save()

    print("✅ PDF created successfully")

if __name__ == "__main__":
    create_pdf()