from typing import TypedDict
from time import perf_counter

from langgraph.graph import END, START, StateGraph

from .rag import build_context, generate_diagnosis
from .retrieval import get_relevant_docs, get_relevant_incidents
from .router import route_query


class IncidentState(TypedDict, total=False):
    user_input: str
    route: str
    incident_query: str | None
    documentation_query: str | None
    retrieved_incidents: list
    retrieved_docs: list
    context: str
    diagnosis: dict
    router_seconds: float
    retrieval_seconds: float
    context_seconds: float
    diagnosis_seconds: float
    total_seconds: float


def router_node(state: IncidentState) -> dict:
    start = perf_counter()
    decision = route_query(state["user_input"])
    return {
        "route": decision.route,
        "incident_query": decision.incident_query,
        "documentation_query": decision.documentation_query,
        "router_seconds": perf_counter() - start,
    }


def retrieve_incidents_node(state: IncidentState) -> dict:
    start = perf_counter()
    incidents = get_relevant_incidents(
        state["incident_query"],
        k=3,
    )
    return {
        "retrieved_incidents": incidents,
        "retrieved_docs": [],
        "retrieval_seconds": perf_counter() - start,
    }


def retrieve_docs_node(state: IncidentState) -> dict:
    start = perf_counter()
    docs = get_relevant_docs(state["documentation_query"], k=4)
    return {
        "retrieved_incidents": [],
        "retrieved_docs": docs,
        "retrieval_seconds": perf_counter() - start,
    }


def retrieve_both_node(state: IncidentState) -> dict:
    start = perf_counter()
    incidents = get_relevant_incidents(state["incident_query"], k=3)
    docs = get_relevant_docs(state["documentation_query"], k=4)
    return {
        "retrieved_incidents": incidents,
        "retrieved_docs": docs,
        "retrieval_seconds": perf_counter() - start,
    }


def direct_node(state: IncidentState) -> dict:
    return {
        "retrieved_incidents": [],
        "retrieved_docs": [],
        "retrieval_seconds": 0.0,
    }


def build_context_node(state: IncidentState) -> dict:
    start = perf_counter()
    return {
        "context": build_context(
            route=state["route"],
            retrieved_incidents=state.get("retrieved_incidents", []),
            retrieved_docs=state.get("retrieved_docs", []),
        ),
        "context_seconds": perf_counter() - start,
    }


def generate_diagnosis_node(state: IncidentState) -> dict:
    start = perf_counter()
    diagnosis = generate_diagnosis(
        user_input=state["user_input"],
        route=state["route"],
        context=state["context"],
    )
    return {
        "diagnosis": diagnosis.model_dump(),
        "diagnosis_seconds": perf_counter() - start,
    }


def choose_route(state: IncidentState) -> str:
    return state["route"]


builder = StateGraph(IncidentState)
builder.add_node("router", router_node)
builder.add_node("retrieve_incidents", retrieve_incidents_node)
builder.add_node("retrieve_docs", retrieve_docs_node)
builder.add_node("retrieve_both", retrieve_both_node)
builder.add_node("direct", direct_node)
builder.add_node("build_context", build_context_node)
builder.add_node("generate_diagnosis", generate_diagnosis_node)

builder.add_edge(START, "router")
builder.add_conditional_edges(
    "router",
    choose_route,
    {
        "historical": "retrieve_incidents",
        "documentation": "retrieve_docs",
        "both": "retrieve_both",
        "direct": "direct",
    },
)
builder.add_edge("retrieve_incidents", "build_context")
builder.add_edge("retrieve_docs", "build_context")
builder.add_edge("retrieve_both", "build_context")
builder.add_edge("direct", "build_context")
builder.add_edge("build_context", "generate_diagnosis")
builder.add_edge("generate_diagnosis", END)

incident_graph = builder.compile()


def run_incident_analysis(user_input: str) -> dict:
    """Invoke the compiled graph once and add the total elapsed time."""
    start = perf_counter()
    result = incident_graph.invoke({"user_input": user_input})
    result["total_seconds"] = perf_counter() - start
    return result
