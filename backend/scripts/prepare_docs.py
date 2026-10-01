import json
import re
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = PROJECT_ROOT / "backend" / "data" / "docs"
OUTPUT_PATH = PROJECT_ROOT / "backend" / "data" / "processed" / "docs_chunks.json"
METADATA_FIELDS = ["title", "source", "url", "product", "topic"]
CHUNK_FIELDS = [
    "chunk_id", "document_id", "title", "source", "url", "product", "topic",
    "chunk_index", "text",
]


def load_document(file_path: Path) -> dict[str, str]:
    """Read front matter and Markdown content from one document."""
    lines = file_path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError(f"Missing front matter in {file_path.name}")

    try:
        end_marker = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration as error:
        raise ValueError(f"Unclosed front matter in {file_path.name}") from error

    metadata = {}
    for line in lines[1:end_marker]:
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip()

    missing_fields = [field for field in METADATA_FIELDS if not metadata.get(field)]
    if missing_fields:
        raise ValueError(f"{file_path.name} is missing metadata: {missing_fields}")

    content = "\n".join(lines[end_marker + 1:])
    return {**{field: metadata[field] for field in METADATA_FIELDS}, "content": content}


def clean_text(text: str) -> str:
    """Remove excess whitespace while keeping Markdown structure and commands."""
    cleaned_lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.splitlines()]
    cleaned_text = "\n".join(cleaned_lines)
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)
    return cleaned_text.strip()


def chunk_text(text: str, chunk_size: int = 500, overlap: int = 75) -> list[str]:
    """Split text into overlapping word-based chunks."""
    if chunk_size <= overlap:
        raise ValueError("chunk_size must be greater than overlap")

    words = text.split()
    chunks = []
    start = 0
    step = chunk_size - overlap

    while start < len(words):
        chunk = " ".join(words[start:start + chunk_size]).strip()
        if chunk:
            chunks.append(chunk)
        start += step

    return chunks


def process_documents() -> list[dict[str, object]]:
    """Load, clean, chunk, and copy metadata for all Markdown documents."""
    all_chunks = []
    document_paths = sorted(DOCS_DIR.glob("*.md"))

    for document_path in document_paths:
        document = load_document(document_path)
        document_id = document_path.stem
        chunks = chunk_text(clean_text(document["content"]))

        for chunk_index, text in enumerate(chunks):
            all_chunks.append({
                "chunk_id": f"{document_id}_{chunk_index:03d}",
                "document_id": document_id,
                "title": document["title"],
                "source": document["source"],
                "url": document["url"],
                "product": document["product"],
                "topic": document["topic"],
                "chunk_index": chunk_index,
                "text": text,
            })

    return all_chunks


def validate_chunks(chunks: list[dict[str, object]]) -> None:
    """Check the minimum fields needed by the next embedding step."""
    chunk_ids = [chunk["chunk_id"] for chunk in chunks]
    if len(chunk_ids) != len(set(chunk_ids)):
        raise ValueError("Chunk IDs must be unique.")

    for chunk in chunks:
        missing_fields = [field for field in CHUNK_FIELDS if not chunk.get(field)]
        if missing_fields:
            raise ValueError(f"Chunk {chunk.get('chunk_id')} is missing: {missing_fields}")


def save_chunks(chunks: list[dict[str, object]]) -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(json.dumps(chunks, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def print_summary(chunks: list[dict[str, object]], document_count: int) -> None:
    print(f"Documents processed: {document_count}")
    print(f"Chunks created: {len(chunks)}")
    print("Chunks by product:")
    product_counts = {}
    for chunk in chunks:
        product_counts[chunk["product"]] = product_counts.get(chunk["product"], 0) + 1
    for product, count in sorted(product_counts.items()):
        print(f"  {product}: {count} chunks")

    print("\nFirst 3 chunks:")
    for chunk in chunks[:3]:
        preview = str(chunk["text"])[:300].replace("\n", " ")
        print(f"\n{chunk['chunk_id']}")
        print(f"title: {chunk['title']}")
        print(f"product: {chunk['product']}")
        print(f"topic: {chunk['topic']}")
        print(f"text preview: {preview}")

    print(f"\nOutput JSON: {OUTPUT_PATH}")


def main() -> None:
    document_paths = sorted(DOCS_DIR.glob("*.md"))
    chunks = process_documents()
    validate_chunks(chunks)
    save_chunks(chunks)
    print_summary(chunks, len(document_paths))


if __name__ == "__main__":
    main()
