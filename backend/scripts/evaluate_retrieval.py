import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.retrieval import retrieve_docs, retrieve_incidents


QUERY_GROUPS = {
    "A - clear in-domain incidents": [
        "PostgreSQL connection refused on port 5432 after server restart",
        "Computer can ping 8.8.8.8 but cannot resolve domain names",
        "Nginx returns 502 Bad Gateway after application deployment",
        "Docker container keeps restarting after startup",
        "Ubuntu server reports no space left on device",
        "Application fails with permission denied when writing logs",
        "Linux server becomes slow and memory usage reaches 98%",
        "Windows workstation cannot reach an internal service on its TCP port",
    ],
    "B - related but general IT queries": [
        "Website is unavailable after deployment",
        "Application cannot communicate with database",
        "Server service does not start after reboot",
        "Users cannot access an internal hostname",
    ],
    "C - unrelated queries": [
        "How do I change my phone wallpaper?",
        "What is the capital of Algeria?",
        "Write a Python program to calculate Fibonacci numbers.",
        "What is today's football score?",
    ],
}


def evaluate_query(query: str) -> tuple[list[dict], list[dict]]:
    incidents = retrieve_incidents(query, k=3)
    docs = retrieve_docs(query, k=4)
    return incidents, docs


def print_results(query: str, incidents: list[dict], docs: list[dict]) -> None:
    print("=" * 50)
    print(f"QUERY:\n{query}")
    print("\nINCIDENT RESULTS")
    for position, result in enumerate(incidents, start=1):
        print(f"{position}. {result['score']:.4f} | {result['ticket_id']} | {result['title']}")

    print("\nDOCUMENTATION RESULTS")
    for position, result in enumerate(docs, start=1):
        print(f"{position}. {result['score']:.4f} | {result['title']}")


def print_summary(rows: list[tuple[str, float, float]]) -> None:
    print("\n" + "=" * 50)
    print("SCORE SUMMARY")
    print(f"{'Query':<58} {'Incident top':>14} {'Docs top':>10}")
    print("-" * 86)
    for query, incident_score, doc_score in rows:
        print(f"{query[:58]:<58} {incident_score:>14.4f} {doc_score:>10.4f}")


def main() -> None:
    summary_rows = []
    for group_name, queries in QUERY_GROUPS.items():
        print(f"\n### {group_name}")
        for query in queries:
            incidents, docs = evaluate_query(query)
            print_results(query, incidents, docs)
            summary_rows.append((query, incidents[0]["score"], docs[0]["score"]))

    print_summary(summary_rows)


if __name__ == "__main__":
    main()
