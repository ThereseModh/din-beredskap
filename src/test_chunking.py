from chunker import load_and_chunk_documents
import random

chunks = load_and_chunk_documents()

print(f"\nTotalt antal chunkar: {len(chunks)}\n")

# Visa tre exempel
for i, example in enumerate(random.sample(chunks, 3), 1):
    print(
        f"Exempel {i} (Källa: {example['source']}):\n{example['content']}\n{'-' * 50}"
    )
