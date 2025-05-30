from pathlib import Path


def split_into_chunks(text, max_length=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_length, len(text))
        chunks.append(text[start:end])
        start += max_length - overlap
    return chunks


def load_and_chunk_documents(data_dir="data"):
    base_path = Path(data_dir)
    all_chunks = []

    for source_folder in base_path.iterdir():
        if source_folder.is_dir():
            source_name = source_folder.name
            for file in source_folder.glob("*.txt"):
                try:
                    text = file.read_text(encoding="utf-8")
                    chunks = split_into_chunks(text)
                    for chunk in chunks:
                        all_chunks.append({"source": source_name, "content": chunk})
                except UnicodeDecodeError as e:
                    print(f"Could not read {file}: {e}")

    return all_chunks
