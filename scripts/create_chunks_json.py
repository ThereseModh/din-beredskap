import json
from pathlib import Path
import sys

# Lägg till src/ i sys.path så vi kan importera chunker.py
sys.path.append(str(Path(__file__).resolve().parent.parent / "src"))

from chunker import load_and_chunk_documents


def main():
    chunks = load_and_chunk_documents(data_dir="data")

    output_path = Path("data/chunks.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"Sparade {len(chunks)} chunks till {output_path}")


if __name__ == "__main__":
    main()
