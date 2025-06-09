import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer, util
import torch

# Sökväg till embeddingsfil
EMBEDDING_FILE = Path("data/chunk_embeddings.pkl")

# Ladda chunks och deras embeddings
try:
    with EMBEDDING_FILE.open("rb") as f:
        chunks, chunk_embeddings = pickle.load(f)
except FileNotFoundError:
    raise RuntimeError(f"Filen {EMBEDDING_FILE} hittades inte.")
except Exception as e:
    raise RuntimeError(f"Misslyckades att läsa embeddings: {e}")

# Ladda modellen
model = SentenceTransformer("all-MiniLM-L6-v2")


def retrieve_context(question: str, top_n: int = 6) -> str:
    """
    Returnerar de mest relevanta textavsnitten för en given fråga baserat på semantisk likhet.

    :param question: Användarens fråga
    :param top_n: Antal textavsnitt att returnera
    :return: Sträng med sammanfogade textavsnitt och källor
    """
    if not chunks or not chunk_embeddings.any():
        return "Inga chunks är tillgängliga för sökning."

    # Skapa embedding för frågan
    question_embedding = model.encode(question, convert_to_tensor=True)

    # Beräkna likheten mellan frågan och alla chunks
    cosine_scores = util.cos_sim(question_embedding, chunk_embeddings)[0]

    # Hämta index på toppmatchningar
    top_indices = torch.topk(cosine_scores, k=top_n).indices

    # Sätt ihop resultat
    selected_chunks = [
        f"{chunks[i]['content']}\nKälla: {chunks[i]['source']}" for i in top_indices
    ]

    return "\n\n".join(selected_chunks)
