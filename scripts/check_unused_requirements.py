import os
import re

REQUIREMENTS_FILE = "requirements.txt"
PROJECT_DIR = "src"  # Sök i denna mapp


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
                                module = match.group(2).split(".")[0]
                                imported.add(module.lower())
                except Exception as e:
                    print(f"⚠️ Kunde inte läsa {file_path}: {e}")
    return imported


# Enkla manuella mappningar mellan pip-paket och modulnamn
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


def clean_package_name(pkg_line):
    return pkg_line.split("==")[0].lower().replace("_", "-")


def map_package_to_module(pkg):
    # Använd alias om det finns, annars försök gissa
    return manual_aliases.get(pkg, pkg.replace("-", "_"))


def main():
    used_modules = list_imported_modules(PROJECT_DIR)
    print(
        f"📄 Hittade {len(used_modules)} importerade moduler i src/: {sorted(used_modules)}\n"
    )

    with open(REQUIREMENTS_FILE, encoding="utf-8") as f:
        packages = [
            line.strip() for line in f if line.strip() and not line.startswith("#")
        ]

    unused_packages = []
    for pkg_line in packages:
        pkg_name = clean_package_name(pkg_line)
        module_guess = map_package_to_module(pkg_name)

        if module_guess not in used_modules:
            unused_packages.append(pkg_line)

    print("📦 Paket i requirements.txt som inte verkar användas:")
    for pkg in unused_packages:
        print("–", pkg)

    if not unused_packages:
        print("✅ Alla paket verkar användas!")


if __name__ == "__main__":
    main()
