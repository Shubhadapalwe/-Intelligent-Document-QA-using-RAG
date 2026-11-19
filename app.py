"""Streamlit entry point for the local document RAG application."""
import streamlit as st
from src.pdf_processing import extract_text_from_pdf, split_text_into_chunks
from src.retrieval import create_vector_database, search_relevant_chunks
from src.llm import ask_llm

st.set_page_config(page_title="Intelligent Document Q&A", page_icon="📄", layout="wide")
st.title("📄 Intelligent Document Question Answering")
st.caption("Local RAG · Sentence Transformers · FAISS · Ollama Llama3")

with st.sidebar:
    st.header("Settings")
    chunk_size = st.slider("Chunk size (characters)", 300, 1800, 900, 100)
    overlap = st.slider("Chunk overlap", 0, 300, 150, 25)
    top_k = st.slider("Relevant chunks", 1, 8, 3)
    st.info("Install Ollama, run `ollama pull llama3`, and ensure the Ollama server is running.")

upload_tab, qa_tab = st.tabs(["📤 Upload document", "💬 Ask questions"])
with upload_tab:
    uploaded_file = st.file_uploader("Choose a text-based PDF", type=["pdf"])
    if uploaded_file is not None and st.button("Process document", type="primary"):
        try:
            with st.spinner("Extracting, chunking, and embedding PDF..."):
                pages = extract_text_from_pdf(uploaded_file)
                chunks = split_text_into_chunks(pages, chunk_size, overlap)
                if not chunks:
                    st.error("No selectable text found. Scanned PDFs require OCR, which is not included.")
                else:
                    index, chunks = create_vector_database(chunks)
                    st.session_state["rag_index"] = index
                    st.session_state["rag_chunks"] = chunks
                    st.session_state["rag_filename"] = uploaded_file.name
                    st.success(f"Indexed {len(chunks)} chunks from {len(pages)} pages.")
        except Exception as exc:
            st.error(f"Could not process PDF: {exc}")
with qa_tab:
    if "rag_index" not in st.session_state:
        st.warning("Upload and process a PDF first.")
    else:
        st.write(f"Document: **{st.session_state['rag_filename']}**")
        question = st.text_input("Ask a question about the PDF")
        if st.button("Get answer", type="primary", disabled=not question.strip()):
            with st.spinner("Searching document and generating an answer..."):
                try:
                    matches = search_relevant_chunks(question, st.session_state["rag_index"], st.session_state["rag_chunks"], top_k)
                    answer = ask_llm(question, matches)
                    st.subheader("Answer")
                    st.write(answer)
                    with st.expander("Retrieved source passages"):
                        for i, match in enumerate(matches, 1):
                            st.markdown(f"**{i}. Page {match['page']} · similarity {match['score']:.3f}**")
                            st.write(match["text"])
                except Exception as exc:
                    st.error(f"Could not answer: {exc}")
