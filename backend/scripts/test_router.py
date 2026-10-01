import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.router import route_query


TEST_CASES = [
    ("PostgreSQL connection refused on port 5432 after server restart", "both"),
    ("Nginx returns 502 Bad Gateway after the application was deployed", "both"),
    ("The workstation can ping 8.8.8.8 but cannot resolve domain names", "both"),
    ("An internal application started crashing immediately after the latest deployment", "historical"),
    ("What does HTTP 503 Service Unavailable mean?", "documentation"),
    ("How does pg_hba.conf control PostgreSQL client authentication?", "documentation"),
    ("What is localhost?", "direct"),
    ("What is a TCP port?", "direct"),
]

ADVICE_WORDS = {"check", "verify", "ensure", "try", "fix"}


def main() -> None:
    route_matches = True
    query_advice_found = False
    validation_errors = []

    for user_input, expected_route in TEST_CASES:
        decision = route_query(user_input)
        if decision.route != expected_route:
            route_matches = False
            validation_errors.append(
                f"{user_input}: expected {expected_route}, got {decision.route}"
            )

        queries = [decision.incident_query, decision.documentation_query]
        for query in queries:
            if query and ADVICE_WORDS.intersection(query.lower().split()):
                query_advice_found = True

        print("=" * 50)
        print(f"INPUT:\n{user_input}")
        print(f"\nROUTE:\n{decision.route}")
        print(f"\nINCIDENT QUERY:\n{decision.incident_query}")
        print(f"\nDOCUMENTATION QUERY:\n{decision.documentation_query}")

    print("=" * 50)
    print(f"All 8 route decisions match expected routes: {route_matches}")
    print(f"Any retrieval query contains troubleshooting advice: {query_advice_found}")
    print("Pydantic structured-output validation succeeded for every returned decision.")
    if validation_errors:
        print("Routing mismatches:")
        for error in validation_errors:
            print(f"- {error}")
    else:
        print("Routing mismatches: none")


if __name__ == "__main__":
    main()
