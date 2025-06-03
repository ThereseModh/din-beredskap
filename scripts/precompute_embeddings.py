import json
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Kör endast detta skript om du har uppdaterat textinnehållet i data/

CHUNKS_FILE = Path("data/chunks.json")
OUTPUT_FILE = Path("data/chunk_embeddings.pkl")
MODEL_NAME = "all-MiniLM-L6-v2"


def main():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(f"Filen {CHUNKS_FILE} hittades inte.")

    with CHUNKS_FILE.open("r", encoding="utf-8") as f:
        chunks = json.load(f)

    if not chunks:
        raise ValueError("Inga chunks att bearbeta.")

    texts = [chunk["content"] for chunk in chunks]

    print(f"Laddar modell '{MODEL_NAME}'...")
    model = SentenceTransformer(MODEL_NAME)

    print(f"Skapar embeddings för {len(texts)} chunks...")
    embeddings = model.encode(texts, convert_to_tensor=True)

    with OUTPUT_FILE.open("wb") as f:
        pickle.dump((chunks, embeddings), f)

    print(f"Sparade embeddings till: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
