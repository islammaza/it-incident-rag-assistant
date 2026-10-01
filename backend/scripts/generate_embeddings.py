import json
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INCIDENTS_PATH = PROJECT_ROOT / "backend" / "data" / "incidents" / "glpi_incidents.csv"
DOCS_PATH = PROJECT_ROOT / "backend" / "data" / "processed" / "docs_chunks.json"
PROCESSED_DIR = PROJECT_ROOT / "backend" / "data" / "processed"
MODEL_NAME = "BAAI/bge-small-en-v1.5"
SEARCH_FIELDS = ["title", "description", "category", "environment", "error_message", "symptoms"]


def load_model() -> SentenceTransformer:
    return SentenceTransformer(MODEL_NAME)


def build_incident_text(row: pd.Series) -> str:
    """Build searchable text without including historical answer fields."""
    return "\n".join([
        f"Title: {row['title']}",
        f"Description: {row['description']}",
        f"Category: {row['category']}",
        f"Environment: {row['environment']}",
        f"Error: {row['error_message']}",
        f"Symptoms: {row['symptoms']}",
    ])


def load_incidents() -> tuple[list[str], list[dict[str, str]]]:
    incidents_df = pd.read_csv(INCIDENTS_PATH, dtype=str).fillna("")
    texts = [build_incident_text(row) for _, row in incidents_df.iterrows()]
    metadata = incidents_df.to_dict(orient="records")
    return texts, metadata


def load_docs() -> tuple[list[str], list[dict[str, object]]]:
    docs = json.loads(DOCS_PATH.read_text(encoding="utf-8"))
    texts = [doc["text"] for doc in docs]
    metadata_fields = [
        "chunk_id", "document_id", "title", "source", "url", "product",
        "topic", "chunk_index", "text",
    ]
    metadata = [{field: doc[field] for field in metadata_fields} for doc in docs]
    return texts, metadata


def encode_texts(model: SentenceTransformer, texts: list[str]) -> np.ndarray:
    return np.asarray(
        model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        ),
        dtype=np.float32,
    )


def validate_embeddings(
    embeddings: np.ndarray,
    metadata: list[dict[str, object]],
    name: str,
) -> None:
    if len(embeddings) != len(metadata):
        raise ValueError(f"{name} embeddings and metadata are not aligned.")
    if not np.isfinite(embeddings).all():
        raise ValueError(f"{name} embeddings contain NaN or infinite values.")


def save_results(
    incident_embeddings: np.ndarray,
    incident_metadata: list[dict[str, str]],
    doc_embeddings: np.ndarray,
    doc_metadata: list[dict[str, object]],
) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    # Each vector keeps the same list position as its metadata for later FAISS lookup.
    np.save(PROCESSED_DIR / "incident_embeddings.npy", incident_embeddings)
    np.save(PROCESSED_DIR / "doc_embeddings.npy", doc_embeddings)
    (PROCESSED_DIR / "incident_metadata.json").write_text(
        json.dumps(incident_metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (PROCESSED_DIR / "doc_metadata.json").write_text(
        json.dumps(doc_metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def show_similarity_example(
    model: SentenceTransformer,
    incident_embeddings: np.ndarray,
    incident_metadata: list[dict[str, str]],
) -> None:
    query = "PostgreSQL connection refused on port 5432 after server restart"
    query_embedding = encode_texts(model, [query])[0]
    scores = incident_embeddings @ query_embedding
    top_indices = np.argsort(scores)[::-1][:3]

    print(f"\nSimilarity example query: {query}")
    print("Top 3 matching historical tickets:")
    for rank, index in enumerate(top_indices, start=1):
        metadata = incident_metadata[index]
        print(f"{rank}. {metadata['ticket_id']} - {metadata['title']}")
        print(f"   similarity: {scores[index]:.4f}")


def print_summary(
    incident_embeddings: np.ndarray,
    incident_metadata: list[dict[str, str]],
    doc_embeddings: np.ndarray,
    doc_metadata: list[dict[str, object]],
) -> None:
    print(f"Embedding model:\n{MODEL_NAME}")
    print(f"\nHistorical incidents:\n{len(incident_metadata)}")
    print(f"Incident embedding shape:\n{incident_embeddings.shape}")
    print(f"\nDocumentation chunks:\n{len(doc_metadata)}")
    print(f"Documentation embedding shape:\n{doc_embeddings.shape}")
    print("\nIncident example:")
    print(incident_metadata[0]["title"])
    print(f"Embedding dimensions:\n{incident_embeddings.shape[1]}")
    print("First 10 values:")
    print(np.array2string(incident_embeddings[0][:10], precision=3, separator=", "))
    print("\nNormalization note: normalize_embeddings=True scales vectors to length 1, so a dot product gives cosine similarity.")


def main() -> None:
    model = load_model()
    incident_texts, incident_metadata = load_incidents()
    doc_texts, doc_metadata = load_docs()

    incident_embeddings = encode_texts(model, incident_texts)
    doc_embeddings = encode_texts(model, doc_texts)

    validate_embeddings(incident_embeddings, incident_metadata, "Incident")
    validate_embeddings(doc_embeddings, doc_metadata, "Documentation")
    save_results(incident_embeddings, incident_metadata, doc_embeddings, doc_metadata)
    print_summary(incident_embeddings, incident_metadata, doc_embeddings, doc_metadata)
    show_similarity_example(model, incident_embeddings, incident_metadata)
    print(f"\nOutput directory: {PROCESSED_DIR}")


if __name__ == "__main__":
    main()
