import json
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

from .config import DOC_RELEVANCE_THRESHOLD, INCIDENT_RELEVANCE_THRESHOLD


PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_DIR = PROJECT_ROOT / "backend" / "data" / "processed"
INDEXES_DIR = PROJECT_ROOT / "backend" / "indexes"
MODEL_NAME = "BAAI/bge-small-en-v1.5"
EMBEDDING_DIMENSION = 384


embedding_model = SentenceTransformer(MODEL_NAME)
incident_index = faiss.read_index(str(INDEXES_DIR / "incident_index.faiss"))
doc_index = faiss.read_index(str(INDEXES_DIR / "doc_index.faiss"))
incident_metadata = json.loads(
    (PROCESSED_DIR / "incident_metadata.json").read_text(encoding="utf-8")
)
doc_metadata = json.loads(
    (PROCESSED_DIR / "doc_metadata.json").read_text(encoding="utf-8")
)

if incident_index.ntotal != len(incident_metadata):
    raise ValueError("Incident index and metadata counts do not match.")
if doc_index.ntotal != len(doc_metadata):
    raise ValueError("Documentation index and metadata counts do not match.")
if incident_index.d != EMBEDDING_DIMENSION or doc_index.d != EMBEDDING_DIMENSION:
    raise ValueError("FAISS indexes do not use 384-dimensional vectors.")


def embed_query(query: str) -> np.ndarray:
    """Convert one query into a normalized float32 vector batch."""
    query = query.strip()
    if not query:
        raise ValueError("Query must not be empty.")

    return np.asarray(
        embedding_model.encode([query], normalize_embeddings=True),
        dtype="float32",
    )


def _search_index(index: faiss.Index, metadata: list[dict], query: str, k: int) -> list[dict]:
    if k <= 0:
        raise ValueError("k must be greater than zero.")

    query_embedding = embed_query(query)
    scores, indices = index.search(query_embedding, min(k, index.ntotal))
    results = []

    for score, index_position in zip(scores[0], indices[0]):
        if index_position == -1:
            continue
        result = dict(metadata[index_position])
        result["score"] = float(score)
        results.append(result)

    return results


def retrieve_incidents(query: str, k: int = 3) -> list[dict]:
    """Return the top matching historical incidents without filtering scores."""
    return _search_index(incident_index, incident_metadata, query, k)


def retrieve_docs(query: str, k: int = 4) -> list[dict]:
    """Return the top matching documentation chunks without filtering scores."""
    return _search_index(doc_index, doc_metadata, query, k)


def filter_incident_results(results: list[dict]) -> list[dict]:
    """Keep incident results at or above the empirical relevance threshold."""
    return [
        result for result in results
        if result["score"] >= INCIDENT_RELEVANCE_THRESHOLD
    ]


def filter_doc_results(results: list[dict]) -> list[dict]:
    """Keep documentation results at or above the empirical relevance threshold."""
    return [
        result for result in results
        if result["score"] >= DOC_RELEVANCE_THRESHOLD
    ]


def get_relevant_incidents(query: str, k: int = 3) -> list[dict]:
    """Retrieve incident results and then apply relevance filtering."""
    return filter_incident_results(retrieve_incidents(query, k))


def get_relevant_docs(query: str, k: int = 4) -> list[dict]:
    """Retrieve documentation results and then apply relevance filtering."""
    return filter_doc_results(retrieve_docs(query, k))
