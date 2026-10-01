import json
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.app.graph import incident_graph

VALID_ROUTES = {"historical", "documentation", "both", "direct"}
VALID_SEVERITIES = {"Low", "Medium", "High", "Critical"}
TEST_CASES_PATH = PROJECT_ROOT / "tests" / "final_test_cases.json"


def validate_metadata(result: dict) -> list[str]:
    errors = []
    for incident in result.get("retrieved_incidents", []):
        for field in ["ticket_id", "title", "score"]:
            if not incident.get(field) and incident.get(field) != 0:
                errors.append(f"Historical evidence missing {field}")
    for document in result.get("retrieved_docs", []):
        for field in ["title", "source", "url", "score"]:
            if not document.get(field) and document.get(field) != 0:
                errors.append(f"Documentation evidence missing {field}")
    return errors


def validate_result(result: dict, expected_route: str) -> list[str]:
    errors = []
    diagnosis = result.get("diagnosis")
    if result.get("route") not in VALID_ROUTES:
        errors.append("Invalid or missing route")
    if result.get("route") != expected_route:
        errors.append(f"Expected route {expected_route}, got {result.get('route')}")
    if not diagnosis:
        errors.append("Missing diagnosis")
    else:
        if not diagnosis.get("category"):
            errors.append("Empty category")
        if diagnosis.get("severity") not in VALID_SEVERITIES:
            errors.append("Invalid severity")
        if not diagnosis.get("likely_cause"):
            errors.append("Empty likely cause")
        if not diagnosis.get("explanation"):
            errors.append("Empty explanation")
        if expected_route in {"historical", "both"} and not diagnosis.get("troubleshooting_steps"):
            errors.append("Incident route has no troubleshooting steps")

    incidents = result.get("retrieved_incidents", [])
    documents = result.get("retrieved_docs", [])
    if expected_route == "historical" and not incidents:
        errors.append("Historical route returned no historical evidence")
    if expected_route == "documentation" and not documents:
        errors.append("Documentation route returned no documentation evidence")
    if expected_route == "both" and (not incidents or not documents):
        errors.append("Both route did not return evidence from both sources")
    if expected_route == "direct" and (incidents or documents):
        errors.append("Direct route returned evidence")
    errors.extend(validate_metadata(result))
    return errors


def main() -> None:
    test_cases = json.loads(TEST_CASES_PATH.read_text(encoding="utf-8"))
    route_matches = 0
    pipeline_failures = 0
    group_totals = {route: [0, 0] for route in VALID_ROUTES}

    for test_case in test_cases:
        print("=" * 50)
        print(f"TEST:\n{test_case['name']}")
        print(f"\nQUERY:\n{test_case['query']}")
        print(f"\nEXPECTED ROUTE:\n{test_case['expected_route']}")
        try:
            result = incident_graph.invoke({"user_input": test_case["query"]})
            errors = validate_result(result, test_case["expected_route"])
            actual_route = result.get("route", "missing")
            route_match = actual_route == test_case["expected_route"]
            route_matches += int(route_match)
            group_totals[test_case["expected_route"]][0] += int(route_match)
            group_totals[test_case["expected_route"]][1] += 1
            print(f"\nACTUAL ROUTE:\n{actual_route}")
            print(f"\nROUTE MATCH:\n{route_match}")
            diagnosis = result.get("diagnosis", {})
            print(f"\nCATEGORY:\n{diagnosis.get('category', 'missing')}")
            print(f"\nSEVERITY:\n{diagnosis.get('severity', 'missing')}")
            print(f"\nHISTORICAL EVIDENCE:\n{len(result.get('retrieved_incidents', []))}")
            print(f"\nDOCUMENTATION EVIDENCE:\n{len(result.get('retrieved_docs', []))}")
            print(f"\nTROUBLESHOOTING STEPS:\n{len(diagnosis.get('troubleshooting_steps', []))}")
            if errors:
                pipeline_failures += 1
                print("\nCHECKS:")
                for error in errors:
                    print(f"- {error}")
            else:
                print("\nCHECKS: passed")
        except Exception as error:
            pipeline_failures += 1
            print(f"\nPIPELINE ERROR: {error}")

    print("=" * 50)
    print("FINAL VALIDATION SUMMARY")
    print(f"\nTests executed: {len(test_cases)}")
    print(f"Route matches: {route_matches}/{len(test_cases)}")
    print(f"Pipeline failures: {pipeline_failures}")
    for route in ["both", "historical", "documentation", "direct"]:
        matches, total = group_totals[route]
        print(f"{route.title()} route tests: {matches}/{total}")
    status = "PASS" if pipeline_failures == 0 and route_matches == len(test_cases) else "REVIEW REQUIRED"
    print(f"\nResult:\n{status}")
    print("=" * 50)


if __name__ == "__main__":
    main()
