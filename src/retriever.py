from pathlib import Path
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict


def retrieve_context(
    question: str, chunks: List[Dict[str, str]], top_n: int = 3
) -> str:
    texts = [chunk["content"] for chunk in chunks]

    vectorizer = TfidfVectorizer().fit(texts + [question])
    chunk_vectors = vectorizer.transform(texts)
    question_vector = vectorizer.transform([question])

    similarities = cosine_similarity(question_vector, chunk_vectors).flatten()
    top_indices = similarities.argsort()[-top_n:][::-1]

    selected = [chunks[i] for i in top_indices]
    return "\n\n".join(
        f"[Källa: {chunk['source']}]\n{chunk['content']}" for chunk in selected
    )
