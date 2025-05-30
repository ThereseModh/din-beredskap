import os
import re

REQUIREMENTS_FILE = "requirements.txt"
PROJECT_DIR = "src"
OUTPUT_FILE = "requirements_clean.txt"

# Mappning mellan pip-paket och deras importnamn
manual_aliases = {
    "scikit-learn": "sklearn",
    "pillow": "PIL",
    "pyyaml": "yaml",
    "python-dotenv": "dotenv",
    "sentence-transformers": "sentence_transformers",
    "typing-extensions": "typing_extensions",
    "pydantic-core": "pydantic_core",
    "pydantic": "pydantic",
    "torch": "torch",
    "transformers": "transformers",
    "tokenizers": "tokenizers",
    "tqdm": "tqdm",
}


def list_imported_modules(project_dir):
    imported = set()
    pattern = re.compile(r"^\s*(import|from)\s+([a-zA-Z0-9_\.]+)")
    for root, _, files in os.walk(project_dir):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, encoding="utf-8") as f:
                        for line in f:
                            match = pattern.match(line)
                            if match:
                                module = match.group(2).split(".")[0].lower()
                                imported.add(module)
                except Exception as e:
                    print(f"⚠️ Kunde inte läsa {file_path}: {e}")
    return imported


def clean_package_name(name):
    return name.split("==")[0].strip().lower().replace("_", "-")


def map_package_to_module(pkg):
    return manual_aliases.get(pkg, pkg.replace("-", "_"))


def main():
    used_modules = list_imported_modules(PROJECT_DIR)
    print(
        f"🔎 Hittade {len(used_modules)} importerade moduler i src/: {sorted(used_modules)}\n"
    )

    with open(REQUIREMENTS_FILE, encoding="utf-8") as f:
        original_packages = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]

    kept_packages = []
    for line in original_packages:
        pkg_name = clean_package_name(line)
        mod_guess = map_package_to_module(pkg_name)
        if mod_guess in used_modules:
            kept_packages.append(line)

    # Skriv den nya requirements_clean.txt
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
        for pkg in kept_packages:
            f_out.write(pkg + "\n")

    print(f"✅ Skapade {OUTPUT_FILE} med {len(kept_packages)} paket:")
    for pkg in kept_packages:
        print("–", pkg)


if __name__ == "__main__":
    main()
