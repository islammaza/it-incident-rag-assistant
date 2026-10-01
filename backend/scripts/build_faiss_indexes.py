import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "backend" / "data" / "processed"
INDEXES_DIR = PROJECT_ROOT / "backend" / "indexes"
EMBEDDING_DIMENSION = 384
MODEL_NAME = "BAAI/bge-small-en-v1.5"
QUERY = "PostgreSQL connection refused on port 5432 after server restart"


def load_inputs() -> tuple[np.ndarray, list[dict], np.ndarray, list[dict]]:
    incident_embeddings = np.load(PROCESSED_DIR / "incident_embeddings.npy").astype("float32")
    doc_embeddings = np.load(PROCESSED_DIR / "doc_embeddings.npy").astype("float32")
    incident_metadata = json.loads(
        (PROCESSED_DIR / "incident_metadata.json").read_text(encoding="utf-8")
    )
    doc_metadata = json.loads(
        (PROCESSED_DIR / "doc_metadata.json").read_text(encoding="utf-8")
    )
    return incident_embeddings, incident_metadata, doc_embeddings, doc_metadata


def validate_inputs(
    incident_embeddings: np.ndarray,
    incident_metadata: list[dict],
    doc_embeddings: np.ndarray,
    doc_metadata: list[dict],
) -> None:
    if incident_embeddings.ndim != 2 or incident_embeddings.shape[1] != EMBEDDING_DIMENSION:
        raise ValueError(f"Incident embeddings must have shape (n, {EMBEDDING_DIMENSION}).")
    if doc_embeddings.ndim != 2 or doc_embeddings.shape[1] != EMBEDDING_DIMENSION:
        raise ValueError(f"Documentation embeddings must have shape (n, {EMBEDDING_DIMENSION}).")
    if len(incident_embeddings) != len(incident_metadata):
        raise ValueError("Incident vectors and metadata are not aligned.")
    if len(doc_embeddings) != len(doc_metadata):
        raise ValueError("Documentation vectors and metadata are not aligned.")
    if not np.isfinite(incident_embeddings).all() or not np.isfinite(doc_embeddings).all():
        raise ValueError("Embeddings contain NaN or infinite values.")


def build_indexes(
    incident_embeddings: np.ndarray,
    doc_embeddings: np.ndarray,
) -> tuple[faiss.IndexFlatIP, faiss.IndexFlatIP]:
    # Normalized embeddings make inner product equivalent to cosine similarity.
    incident_index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
    doc_index = faiss.IndexFlatIP(EMBEDDING_DIMENSION)
    incident_index.add(incident_embeddings)
    doc_index.add(doc_embeddings)
    return incident_index, doc_index


def save_and_reload_indexes(
    incident_index: faiss.IndexFlatIP,
    doc_index: faiss.IndexFlatIP,
) -> tuple[faiss.Index, faiss.Index]:
    INDEXES_DIR.mkdir(parents=True, exist_ok=True)
    incident_path = INDEXES_DIR / "incident_index.faiss"
    doc_path = INDEXES_DIR / "doc_index.faiss"
    faiss.write_index(incident_index, str(incident_path))
    faiss.write_index(doc_index, str(doc_path))
    return faiss.read_index(str(incident_path)), faiss.read_index(str(doc_path))


def run_search_test(
    incident_index: faiss.Index,
    incident_metadata: list[dict],
) -> None:
    model = SentenceTransformer(MODEL_NAME)
    query_embedding = model.encode(
        [QUERY],
        normalize_embeddings=True,
        show_progress_bar=False,
    ).astype("float32")
    scores, indices = incident_index.search(query_embedding, 3)

    print(f"\nQuery:\n{QUERY}")
    print("\nTop 3 FAISS results:")
    for rank, (score, index) in enumerate(zip(scores[0], indices[0]), start=1):
        metadata = incident_metadata[index]
        print(f"\n{rank}. {metadata['ticket_id']}")
        print(f"   Title: {metadata['title']}")
        print(f"   Similarity: {score:.4f}")


def main() -> None:
    incident_embeddings, incident_metadata, doc_embeddings, doc_metadata = load_inputs()
    validate_inputs(incident_embeddings, incident_metadata, doc_embeddings, doc_metadata)
    incident_index, doc_index = build_indexes(incident_embeddings, doc_embeddings)

    if incident_index.ntotal != len(incident_metadata):
        raise ValueError("Incident FAISS index count does not match metadata count.")
    if doc_index.ntotal != len(doc_metadata):
        raise ValueError("Documentation FAISS index count does not match metadata count.")

    loaded_incident_index, loaded_doc_index = save_and_reload_indexes(incident_index, doc_index)
    if loaded_incident_index.ntotal != incident_index.ntotal:
        raise ValueError("Reloaded incident index count does not match saved index.")
    if loaded_doc_index.ntotal != doc_index.ntotal:
        raise ValueError("Reloaded documentation index count does not match saved index.")

    print(f"Embedding dimension: {EMBEDDING_DIMENSION}")
    print(f"\nIncident vectors: {len(incident_embeddings)}")
    print(f"Incident FAISS index: {incident_index.ntotal} vectors")
    print(f"\nDocumentation vectors: {len(doc_embeddings)}")
    print(f"Documentation FAISS index: {doc_index.ntotal} vectors")
    print(f"\nIndexes saved:")
    print(INDEXES_DIR / "incident_index.faiss")
    print(INDEXES_DIR / "doc_index.faiss")
    print("\nReload validation: both FAISS indexes loaded successfully.")

    run_search_test(loaded_incident_index, incident_metadata)


if __name__ == "__main__":
    main()
