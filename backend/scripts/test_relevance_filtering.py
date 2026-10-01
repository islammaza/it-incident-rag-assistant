import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.retrieval import (
    get_relevant_docs,
    get_relevant_incidents,
    retrieve_docs,
    retrieve_incidents,
)


QUERIES = [
    "PostgreSQL connection refused on port 5432 after server restart",
    "Nginx returns 502 Bad Gateway after deployment",
    "Application cannot communicate with database",
    "What is the capital of Algeria?",
    "How do I change the wallpaper on my phone?",
]


def print_results(query: str) -> None:
    raw_incidents = retrieve_incidents(query)
    relevant_incidents = get_relevant_incidents(query)
    raw_docs = retrieve_docs(query)
    relevant_docs = get_relevant_docs(query)

    print("=" * 50)
    print(f"QUERY:\n{query}")
    print(f"\nRaw incident results: {len(raw_incidents)}")
    print(f"Relevant incident results: {len(relevant_incidents)}")
    print("\nRelevant incidents:")
    for result in relevant_incidents:
        print(f"{result['score']:.4f} | {result['ticket_id']} | {result['title']}")

    print(f"\nRaw docs results: {len(raw_docs)}")
    print(f"Relevant docs results: {len(relevant_docs)}")
    print("\nRelevant docs:")
    for result in relevant_docs:
        print(f"{result['score']:.4f} | {result['title']}")


def main() -> None:
    for query in QUERIES:
        print_results(query)


if __name__ == "__main__":
    main()
