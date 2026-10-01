import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.graph import incident_graph


TEST_CASES = [
    ("PostgreSQL connection refused on port 5432 after server restart", "both"),
    ("Nginx returns 502 Bad Gateway after deployment", "both"),
    ("An internal application started crashing immediately after the latest deployment", "historical"),
    ("What does HTTP 503 Service Unavailable mean?", "documentation"),
    ("What is localhost?", "direct"),
]


def print_result(user_input: str, expected_route: str) -> bool:
    result = incident_graph.invoke({"user_input": user_input})
    route_matches = result["route"] == expected_route

    print("=" * 50)
    print(f"INPUT:\n{user_input}")
    print(f"\nROUTE:\n{result['route']} (expected: {expected_route})")
    print(f"\nINCIDENT QUERY:\n{result.get('incident_query')}")
    print(f"\nDOCUMENTATION QUERY:\n{result.get('documentation_query')}")
    print(f"\nRETRIEVED INCIDENTS: {len(result.get('retrieved_incidents', []))}")
    for position, incident in enumerate(result.get("retrieved_incidents", []), start=1):
        print(f"{position}. {incident['ticket_id']} | score {incident['score']:.4f} | {incident['title']}")

    print(f"\nRETRIEVED DOCUMENTS: {len(result.get('retrieved_docs', []))}")
    for position, document in enumerate(result.get("retrieved_docs", []), start=1):
        print(f"{position}. {document['title']} | score {document['score']:.4f}")

    print(f"\nROUTE MATCH: {route_matches}")
    return route_matches


def main() -> None:
    matches = [print_result(user_input, expected) for user_input, expected in TEST_CASES]
    print("=" * 50)
    print(f"All route expectations matched: {all(matches)}")
    print("LangGraph workflow completed without errors.")


if __name__ == "__main__":
    main()
