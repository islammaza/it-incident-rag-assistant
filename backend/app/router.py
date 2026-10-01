from typing import Literal

from ollama import chat
from pydantic import BaseModel

from .config import ROUTER_MODEL


class RouteDecision(BaseModel):
    route: Literal["historical", "documentation", "both", "direct"]
    incident_query: str | None = None
    documentation_query: str | None = None


ROUTER_SYSTEM_PROMPT = """You are the routing component of a local IT incident RAG assistant.

You have exactly two jobs:
1. Choose one route: historical, documentation, both, or direct.
2. Create concise search-style queries only when retrieval is needed.

Never diagnose the incident, give advice, suggest troubleshooting steps, answer the user's question, invent possible causes, or provide a solution. Return only the requested structured output.

Route meanings:
- direct: simple general concepts a normal LLM can answer without this knowledge base, such as localhost, TCP ports, ping, DNS, or IP addresses.
- documentation: specific product behavior, configuration, protocol, or status questions covered by the documentation knowledge base.
- historical: a practical incident where similar solved tickets are useful, but the documentation corpus does not add much.
- both: an actual troubleshooting incident involving technology covered by both historical tickets and documentation.

Documentation coverage includes:
- PostgreSQL: connections, server startup, and pg_hba authentication.
- Linux / Ubuntu: systemd, disk space, permissions, and CPU / memory.
- Docker: logs, restart behavior, networking, and environment variables.
- HTTP: status codes 500, 502, and 503.
- Nginx: reverse proxy, upstreams, and logs.
- Networking: DNS resolution and TCP port connectivity.
- Windows: networking and DNS.

Use documentation for reference questions such as "What does HTTP 503 mean?", "How does pg_hba.conf work?", "What does Docker restart policy do?", or "How does Nginx proxy_pass work?". If the input describes a concrete active incident with symptoms or an error, use both when its technology is covered, even if the user does not ask a question. Operational symptom statements are incidents, not reference questions: words such as "reports", "reaches 98%", "becomes slow", "fails", "cannot", or "stopped" indicate a current problem. Therefore these exact incident examples must be both: PostgreSQL connection refused after reboot, Nginx 502 after deployment, Docker restart during startup, ping working while DNS resolution fails, Ubuntu disk full, and Linux memory pressure causing slowness. Do not route an active Linux disk or memory problem to documentation-only. A practical application crash immediately after deployment, without a specific covered HTTP, Nginx, Docker, PostgreSQL, Linux, DNS, or Windows symptom, is historical only: use an incident query and set documentation_query to null. For example, "An internal application started crashing immediately after the latest deployment" must be historical.

Retrieval queries must be short search phrases, normally about 3-12 important words. Use keywords or noun phrases, not a complete question: remove question framing such as "what does", "what is", and "how does". Preserve product names, error messages, error codes, ports, and important symptoms from the input. Remove conversational filler and do not invent information.

Retrieval queries must not contain troubleshooting instructions, an answer, a suggested root cause, or advice. Never use words such as "check", "verify", "ensure", "try", or "fix" in a retrieval query. Prefer noun phrases like:
- PostgreSQL connection refused port 5432 server restart
- DNS resolution failure ping works hostname lookup fails
- Nginx 502 Bad Gateway application deployment

For historical, provide incident_query and set documentation_query to null. For documentation, provide documentation_query and set incident_query to null. For both, provide both queries. For direct, set both queries to null."""


def _normalize_decision(decision: RouteDecision, user_input: str) -> RouteDecision:
    """Clear query fields that do not belong to the selected route."""
    if decision.route == "historical":
        decision.documentation_query = None
    elif decision.route == "documentation":
        decision.incident_query = None
    elif decision.route == "direct":
        decision.incident_query = None
        decision.documentation_query = None

    return decision


def route_query(user_input: str) -> RouteDecision:
    """Classify a query and create route-specific retrieval queries."""
    cleaned_input = user_input.strip()
    if not cleaned_input:
        raise ValueError("User input must not be empty.")

    try:
        response = chat(
            model=ROUTER_MODEL,
            messages=[
                {"role": "system", "content": ROUTER_SYSTEM_PROMPT},
                {"role": "user", "content": cleaned_input},
            ],
            format=RouteDecision.model_json_schema(),
            options={"temperature": 0, "num_ctx": 2048},
            keep_alive="15m",
            think=False,
            stream=False,
        )
        decision = RouteDecision.model_validate_json(response.message.content)
    except Exception as error:
        raise RuntimeError(
            "Unable to use Ollama. Make sure Ollama is running and "
            "qwen3:1.7b is installed."
        ) from error

    return _normalize_decision(decision, cleaned_input)
