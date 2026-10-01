import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.graph import incident_graph


TEST_CASES = [
    "PostgreSQL connection refused on port 5432 after server restart",
    "An internal application started crashing immediately after the latest deployment",
    "What does HTTP 503 Service Unavailable mean?",
    "What is localhost?",
]


def print_result(user_input: str) -> None:
    result = incident_graph.invoke({"user_input": user_input})
    diagnosis = result["diagnosis"]

    print("=" * 60)
    print(f"INPUT:\n{user_input}")
    print(f"\nROUTE: {result['route']}")
    print(f"Historical incidents: {len(result.get('retrieved_incidents', []))}")
    print(f"Documentation chunks: {len(result.get('retrieved_docs', []))}")
    print(f"\nCATEGORY\n{diagnosis['category']}")
    print(f"\nSEVERITY\n{diagnosis['severity']}")
    print(f"\nLIKELY CAUSE\n{diagnosis['likely_cause']}")
    print(f"\nEXPLANATION\n{diagnosis['explanation']}")
    print("\nTROUBLESHOOTING STEPS")
    for position, step in enumerate(diagnosis["troubleshooting_steps"], start=1):
        print(f"{position}. {step}")

    print("\nHISTORICAL EVIDENCE")
    for incident in result.get("retrieved_incidents", []):
        print(f"{incident['ticket_id']} | {incident['title']} | score {incident['score']:.4f}")

    print("\nDOCUMENTATION SOURCES")
    for document in result.get("retrieved_docs", []):
        print(f"{document['title']} | URL: {document['url']} | score {document['score']:.4f}")


def main() -> None:
    for user_input in TEST_CASES:
        print_result(user_input)

    print("=" * 60)
    print("LangGraph RAG pipeline completed without errors.")
    print("Pydantic diagnosis validation completed through DiagnosisResult.")


if __name__ == "__main__":
    main()
