import json
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Detta skript ska köras när textinnehållet i data/ har uppdaterats.
# Det genererar och sparar embeddings för alla chunks.

CHUNKS_FILE = Path("data/chunks.json")  # Källa med färdigchunkad text
OUTPUT_FILE = Path("data/chunk_embeddings.pkl")  # Målfil där embeddings ska sparas
MODEL_NAME = "all-MiniLM-L6-v2"  # Förtränad modell från Hugging Face


def main():
    # Kontrollerar att filen med chunks finns
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(f"Filen {CHUNKS_FILE} hittades inte.")

    # Läser in textavsnitten (chunks) från JSON-fil
    with CHUNKS_FILE.open("r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        raise ValueError("Inga chunks att bearbeta.")

    # Extraherar själva textinnehållet från varje chunk
    texts = [chunk["content"] for chunk in chunks]

    # Laddar förtränad sentence-transformer-modell
    print(f"Laddar modell '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    # Skapar embeddings för alla textavsnitt
    print(f"Skapar embeddings för {len(texts)} chunks...")
    embeddings = model.encode(texts, convert_to_tensor=True)

    # Sparar både chunks och embeddings som binärfil (pickle)
    with OUTPUT_FILE.open("wb") as f:
        pickle.dump((chunks, embeddings), f)

    print(f"Sparade embeddings till: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
