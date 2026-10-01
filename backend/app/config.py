from pathlib import Path


BACKEND_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BACKEND_DIR / "data"
INDEXES_DIR = BACKEND_DIR / "indexes"

# Initial empirical thresholds from the Step 8 evaluation queries.
INCIDENT_RELEVANCE_THRESHOLD = 0.60
DOC_RELEVANCE_THRESHOLD = 0.58
ROUTER_MODEL = "qwen3:1.7b"
DIAGNOSIS_MODEL = "qwen3:4b-instruct-2507-q4_K_M"
