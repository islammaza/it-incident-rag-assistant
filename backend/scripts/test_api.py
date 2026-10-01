import requests


BASE_URL = "http://127.0.0.1:8000"


def print_diagnosis(incident: str) -> None:
    response = requests.post(
        f"{BASE_URL}/api/diagnose",
        json={"incident": incident},
        timeout=180,
    )
    response.raise_for_status()
    data = response.json()
    diagnosis = data["diagnosis"]

    print(f"\nIncident: {incident}")
    print(f"HTTP status: {response.status_code}")
    print(f"Route: {data['route']}")
    print(f"Category: {diagnosis['category']}")
    print(f"Severity: {diagnosis['severity']}")
    print(f"Likely cause: {diagnosis['likely_cause']}")
    print(f"Troubleshooting steps: {len(diagnosis['troubleshooting_steps'])}")
    print(f"Historical incidents: {len(data['historical_incidents'])}")
    print(f"Documentation sources: {len(data['documentation'])}")


def main() -> None:
    health_response = requests.get(f"{BASE_URL}/health", timeout=10)
    health_response.raise_for_status()
    print(f"Health status: {health_response.status_code} {health_response.json()}")

    print_diagnosis("PostgreSQL connection refused on port 5432 after server restart")
    print_diagnosis("What is localhost?")


if __name__ == "__main__":
    main()
