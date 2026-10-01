import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.retrieval import retrieve_docs, retrieve_incidents


QUERIES = [
    "PostgreSQL connection refused on port 5432 after server restart",
    "Computer can ping IP addresses but cannot resolve domain names",
    "Docker container keeps restarting because the application exits during startup",
    "Nginx returns 502 Bad Gateway after application deployment",
]


def print_results(query: str) -> None:
    print("=" * 50)
    print(f"QUERY:\n{query}")

    print("\nHISTORICAL INCIDENTS")
    for position, result in enumerate(retrieve_incidents(query), start=1):
        print(f"\n{position}. {result['ticket_id']}")
        print(f"   Title: {result['title']}")
        print(f"   Category: {result['category']}")
        print(f"   Score: {result['score']:.4f}")
        print(f"   Root cause: {result['root_cause']}")

    print("\nDOCUMENTATION")
    for position, result in enumerate(retrieve_docs(query), start=1):
        preview = result["text"][:180].replace("\n", " ")
        print(f"\n{position}. {result['title']}")
        print(f"   Product: {result['product']}")
        print(f"   Topic: {result['topic']}")
        print(f"   Score: {result['score']:.4f}")
        print(f"   Source: {result['source']}")
        print(f"   URL: {result['url']}")
        print(f"   Preview: {preview}...")


def main() -> None:
    for query in QUERIES:
        print_results(query)


if __name__ == "__main__":
    main()
