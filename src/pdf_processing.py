"""PDF extraction and overlapping character-based chunking."""
from PyPDF2 import PdfReader


def extract_text_from_pdf(uploaded_file):
    """Return non-empty PDF pages with 1-based page numbers."""
    reader = PdfReader(uploaded_file)
    pages = []
    for number, page in enumerate(reader.pages, 1):
        content = (page.extract_text() or "").strip()
        if content:
            pages.append({"page": number, "text": content})
    return pages


def split_text_into_chunks(pages, chunk_size=900, overlap=150):
    """Split each page into overlapping text chunks, preserving page metadata."""
    if chunk_size <= 0 or not 0 <= overlap < chunk_size:
        raise ValueError("Require chunk_size > 0 and 0 <= overlap < chunk_size")
    chunks = []
    for page in pages:
        text = page["text"]
        step = chunk_size - overlap
        for start in range(0, len(text), step):
            chunk = text[start:start + chunk_size].strip()
            if chunk:
                chunks.append({"page": page["page"], "text": chunk})
            if start + chunk_size >= len(text):
                break
    return chunks
