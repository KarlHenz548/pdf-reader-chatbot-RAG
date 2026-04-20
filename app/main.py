import streamlit as st
from rag_pipeline import build_index, generate_answer
import tempfile

st.set_page_config(page_title="RAG Chatbot", page_icon="🧠")

st.title("🧠 PDF RAG Chatbot")

# Initialize session memory
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "index_ready" not in st.session_state:
    st.session_state.index_ready = False

# 📄 Upload PDF
uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and not st.session_state.index_ready:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        pdf_path = tmp.name

    st.info("Processing PDF...")

    build_index(pdf_path)

    st.session_state.index_ready = True
    st.success("PDF ready! You can now ask questions.")

# 💬 Chat input
user_input = st.text_input("Ask a question:")

if user_input and st.session_state.index_ready:
    answer = generate_answer(user_input)

    st.session_state.chat_history.append(("You", user_input))
    st.session_state.chat_history.append(("AI", answer))

# Display chat history
for role, msg in st.session_state.chat_history:
    if role == "You":
        st.markdown(f"**🧑 You:** {msg}")
    else:
        st.markdown(f"**🤖 AI:** {msg}")