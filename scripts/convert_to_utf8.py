from pathlib import Path

data_path = Path("data")

for file in data_path.rglob("*.txt"):
    try:
        content = file.read_text(encoding="cp1252")
        file.write_text(content, encoding="utf-8")
        print(f"Konverterade: {file}")
    except Exception as e:
        print(f"Misslyckades: {file} — {e}")
