from sentence_transformers import SentenceTransformer, util
from typing import List, Dict

# Ladda modellen en gång vid uppstart
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_context(
    question: str, chunks: List[Dict[str, str]], top_n: int = 3
) -> str:
    """
    Hittar de mest relevanta textavsnitten (chunks) för en given fråga baserat på semantisk likhet.

    :param question: Frågan från användaren
    :param chunks: Lista med dicts som har "content" och "source"
    :param top_n: Antal mest relevanta chunks att hämta
    :return: En sträng med de mest relevanta textavsnitten och deras källor
    """

    # Extrahera själva texterna från chunks
    texts = [chunk["content"] for chunk in chunks]

    # Skapa embeddings
    chunk_embeddings = model.encode(texts, convert_to_tensor=True)
    question_embedding = model.encode(question, convert_to_tensor=True)

    # Beräkna likheten mellan fråga och varje chunk
    cosine_scores = util.cos_sim(question_embedding, chunk_embeddings)[0]

    # Hämta index för de mest relevanta chunksen
    top_indices = cosine_scores.argsort(descending=True)[:top_n]

    # Kombinera text + källa
    selected_chunks = [
        f"{chunks[i]['content']}\nKälla: {chunks[i]['source']}" for i in top_indices
    ]

    return "\n\n".join(selected_chunks)
