from pathlib import Path


def split_into_chunks(
    text: str, max_length: int = 500, overlap: int = 100
) -> list[str]:
    """
    Delar upp en lång text i överlappande mindre textbitar (chunks).

    :param text: Originaltexten som ska delas.
    :param max_length: Maxlängd per chunk.
    :param overlap: Antal tecken som överlappar mellan två chunks.
    :return: En lista med textchunks.
    """
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + max_length, len(text))
        chunks.append(text[start:end])
        start += max_length - overlap
    return chunks


def load_and_chunk_documents(data_dir: str = "data") -> list[dict]:
    """
    Läser alla .txt-filer i en mappstruktur, delar dem i chunks och lägger till källinformation.

    :param data_dir: Sökväg till huvudmappen med underkataloger innehållande .txt-filer.
    :return: En lista med dictar innehållande 'source' och 'content'.
    """
    base_path = Path(data_dir)
    all_chunks = []

    for source_folder in base_path.iterdir():
        if source_folder.is_dir():
            source_name = source_folder.name
            for file in source_folder.glob("*.txt"):
                try:
                    text = file.read_text(encoding="utf-8")
                    chunks = split_into_chunks(text)
                    all_chunks.extend(
                        {"source": source_name, "content": chunk} for chunk in chunks
                    )
                except UnicodeDecodeError as e:
                    print(f"Kunde inte läsa {file}: {e}")
                except Exception as e:
                    print(f"Oväsentligt fel vid läsning av {file}: {e}")

    return all_chunks
