from ollama import chat

from .config import DIAGNOSIS_MODEL
from .schemas import DiagnosisResult


DIAGNOSIS_SYSTEM_PROMPT = """You are an IT incident diagnosis and troubleshooting assistant.

First distinguish an actual incident from an informational or conceptual technical question. An actual incident reports a failure, symptom, error, outage, or degraded service, such as PostgreSQL connection refused, Nginx 502, an application crash after deployment, or a full disk. For an actual incident, use the current incident and retrieved evidence to produce a cautious structured diagnosis with category, severity, likely cause, explanation, and practical ordered troubleshooting steps.

An informational question asks for a definition, explanation, or product reference and does not report that the user is experiencing a failure. Examples include "What is localhost?", "What is a TCP port?", "What does HTTP 503 Service Unavailable mean?", and "How does pg_hba.conf authentication work?" For an informational question, do not invent an incident, symptoms, outage, or likely cause. This rule has priority even when retrieved documentation describes how to troubleshoot that topic: explain the concept only, do not turn documentation advice into steps. Set severity to Low, set likely_cause exactly to "Not applicable — informational query", directly answer the question in explanation, and return troubleshooting_steps exactly as an empty list [].

Historical incidents are examples, not proof that the current incident has the same root cause. Use retrieved documentation when it supports the explanation or steps. Do not invent evidence, URLs, or confirmed causes. Do not claim a cause is confirmed unless the supplied incident or evidence confirms it. Do not assume a historical solution will necessarily solve the current incident.

When incident evidence is incomplete, use cautious language such as likely, may, could, or the evidence suggests, and say when more diagnostics are needed. Incident troubleshooting steps must verify assumptions before configuration changes, prefer safe diagnostic actions, and avoid destructive or risky actions. Keep the explanation concise and provide 3-6 troubleshooting steps for actual incidents. For direct questions, use general technical knowledge because retrieval may be intentionally empty. Estimate incident severity conservatively and reserve Critical for a widespread business-critical outage. Return only the requested DiagnosisResult structure."""


def build_context(
    route: str,
    retrieved_incidents: list[dict],
    retrieved_docs: list[dict],
) -> str:
    """Format retrieved evidence for the diagnosis model without adding new facts."""
    if route == "direct":
        return "No retrieval was requested for this query."

    sections = []
    if retrieved_incidents:
        for position, incident in enumerate(retrieved_incidents, start=1):
            sections.append(
                "\n".join([
                    f"HISTORICAL INCIDENT {position}",
                    f"Ticket ID: {incident['ticket_id']}",
                    f"Title: {incident['title']}",
                    f"Category: {incident['category']}",
                    f"Environment: {incident['environment']}",
                    f"Error: {incident['error_message']}",
                    f"Symptoms: {incident['symptoms']}",
                    f"Historical root cause: {incident['root_cause']}",
                    f"Historical solution: {incident['solution']}",
                ])
            )
    else:
        sections.append("No relevant historical incidents were retrieved.")

    if retrieved_docs:
        for position, document in enumerate(retrieved_docs, start=1):
            sections.append(
                "\n".join([
                    f"DOCUMENTATION {position}",
                    f"Title: {document['title']}",
                    f"Source: {document['source']}",
                    f"Product: {document['product']}",
                    f"Topic: {document['topic']}",
                    f"Content:\n{document['text']}",
                ])
            )
    else:
        sections.append("No relevant technical documentation was retrieved.")

    return "\n\n".join(sections)


def generate_diagnosis(
    user_input: str,
    route: str,
    context: str,
) -> DiagnosisResult:
    """Generate and validate one structured diagnosis with the local Qwen model."""
    user_prompt = f"""CURRENT INCIDENT

{user_input}

ROUTE

{route}

RETRIEVED EVIDENCE

{context}

TASK

Produce a structured IT diagnosis containing a compatible category, conservative severity, cautious likely cause, concise evidence-based explanation, and 3-6 ordered troubleshooting steps for actual incidents. Do not include source URLs in the diagnosis; the application keeps the retrieved evidence separately."""

    try:
        response = chat(
            model=DIAGNOSIS_MODEL,
            messages=[
                {"role": "system", "content": DIAGNOSIS_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            format=DiagnosisResult.model_json_schema(),
            options={"temperature": 0.2, "num_ctx": 4096},
            keep_alive="15m",
            think=False,
            stream=False,
        )
        return DiagnosisResult.model_validate_json(response.message.content)
    except Exception as error:
        raise RuntimeError(
            "Unable to use the diagnosis model. Make sure Ollama is running and "
            "qwen3:4b-instruct-2507-q4_K_M is installed."
        ) from error
