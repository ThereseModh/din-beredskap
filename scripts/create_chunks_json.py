import json
from pathlib import Path
import sys

# Lägg till src/ i sökvägen för att kunna importera chunker.py
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))
from chunker import load_and_chunk_documents

DATA_DIR = Path("data")
OUTPUT_FILE = DATA_DIR / "chunks.json"


def main():
    print("Chunkar textfiler från data/...")

    chunks = load_and_chunk_documents(data_dir=str(DATA_DIR))

    if not chunks:
        print(
            "Inga chunks genererades. Kontrollera att .txt-filer finns i undermappar."
        )
        return

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open("w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Sparade {len(chunks)} chunks till {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
