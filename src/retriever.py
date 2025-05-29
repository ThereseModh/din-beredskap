from pathlib import Path


def retrieve_context(query: str, data_dir: str = "data") -> str:
    all_text = ""
    for file in Path(data_dir).glob("*.txt"):
        all_text += file.read_text(encoding="utf-8") + "\n"

    return all_text
