import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.graph import run_incident_analysis


POSTGRES_QUERY = "PostgreSQL connection refused on port 5432 after server restart"
DIRECT_QUERY = "What is localhost?"


def print_timing(label: str, query: str, result: dict) -> None:
    print("=" * 50)
    print(f"{label}")
    print(f"QUERY:\n{query}")
    print(f"\nROUTE: {result['route']}")
    print(f"\nRouter:        {result.get('router_seconds', 0.0):.2f} s")
    print(f"Retrieval:     {result.get('retrieval_seconds', 0.0):.2f} s")
    print(f"Context:       {result.get('context_seconds', 0.0):.2f} s")
    print(f"Diagnosis:     {result.get('diagnosis_seconds', 0.0):.2f} s")
    print("--------------------------------")
    print(f"Total:         {result.get('total_seconds', 0.0):.2f} s")
    print(f"Historical evidence: {len(result.get('retrieved_incidents', []))}")
    print(f"Documentation evidence: {len(result.get('retrieved_docs', []))}")


def main() -> None:
    print("Run `ollama ps` before and after this script to inspect model residency.")
    first_result = run_incident_analysis(POSTGRES_QUERY)
    print_timing("RUN 1 - PostgreSQL", POSTGRES_QUERY, first_result)

    second_result = run_incident_analysis(POSTGRES_QUERY)
    print_timing("RUN 2 - PostgreSQL", POSTGRES_QUERY, second_result)

    direct_result = run_incident_analysis(DIRECT_QUERY)
    print_timing("DIRECT - localhost", DIRECT_QUERY, direct_result)

    print("=" * 50)
    print("The default retrieval counts remain 3 incidents and 4 documentation chunks.")
    print("A 2+3 comparison was not made automatically; evidence quality should be compared alongside latency before changing defaults.")


if __name__ == "__main__":
    main()
