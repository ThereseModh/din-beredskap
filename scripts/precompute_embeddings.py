import json
import pickle
from pathlib import Path
from sentence_transformers import SentenceTransformer

# Ladda chunks från fil
chunks_path = Path("data/chunks.json")
with chunks_path.open("r", encoding="utf-8") as f:
    chunks = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")
texts = [chunk["content"] for chunk in chunks]
embeddings = model.encode(texts)

# Spara embeddings + chunks till .pkl
output_path = Path("data/chunk_embeddings.pkl")
with output_path.open("wb") as f:
    pickle.dump((chunks, embeddings), f)

print(f"Sparade {len(chunks)} chunks till {output_path}")
