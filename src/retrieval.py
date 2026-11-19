"""SentenceTransformer embeddings and FAISS cosine similarity retrieval."""
from functools import lru_cache
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(MODEL_NAME)


def create_vector_database(chunks):
    if not chunks:
        raise ValueError("Cannot index an empty document")
    embeddings = get_embedding_model().encode([item["text"] for item in chunks], convert_to_numpy=True)
    vectors = np.asarray(embeddings, dtype=np.float32)
    faiss.normalize_L2(vectors)
    index = faiss.IndexFlatIP(vectors.shape[1])
    index.add(vectors)
    return index, chunks


def search_relevant_chunks(question, index, chunks, top_k=3):
    if not question.strip():
        raise ValueError("Question cannot be empty")
    query = np.asarray(get_embedding_model().encode([question], convert_to_numpy=True), dtype=np.float32)
    faiss.normalize_L2(query)
    scores, positions = index.search(query, min(max(1, top_k), len(chunks)))
    return [{**chunks[int(i)], "score": float(score)} for i, score in zip(positions[0], scores[0]) if i >= 0]
