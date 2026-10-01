import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = PROJECT_ROOT / "backend" / "data" / "docs"
MANIFEST_PATH = DOCS_DIR / "sources.json"
REQUIRED_FIELDS = ["title", "source", "url", "product", "topic"]


def main() -> None:
    markdown_files = sorted(DOCS_DIR.glob("*.md"))
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    manifest_files = {entry["file"] for entry in manifest}

    if not markdown_files:
        raise ValueError("No Markdown documentation files found.")

    for document_path in markdown_files:
        content = document_path.read_text(encoding="utf-8")
        missing_fields = [
            field for field in REQUIRED_FIELDS
            if not any(line.startswith(f"{field}:") for line in content.splitlines())
        ]
        if missing_fields:
            raise ValueError(f"{document_path.name} is missing: {missing_fields}")
        if document_path.name not in manifest_files:
            raise ValueError(f"{document_path.name} is missing from sources.json")

        product = next(
            line.split(":", 1)[1].strip()
            for line in content.splitlines()
            if line.startswith("product:")
        )
        print(f"{document_path.name}: {product}")

    markdown_names = {path.name for path in markdown_files}
    missing_documents = markdown_names - manifest_files
    extra_manifest_files = manifest_files - markdown_names
    if missing_documents or extra_manifest_files:
        raise ValueError(
            f"Manifest mismatch. Missing: {missing_documents}; "
            f"extra: {extra_manifest_files}"
        )

    print(f"Validated {len(markdown_files)} documentation files.")


if __name__ == "__main__":
    main()
