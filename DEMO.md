# Internship Demo Guide

## Main Demo

1. Start Ollama and verify the two models are available.
2. Run `ollama ps` once before testing if you want to show model residency.
3. Open a terminal in `backend/` and run `uvicorn app.main:app --reload`.
4. Open another terminal in `frontend/` and run `npm run dev`.
5. Open the Vite URL, normally `http://localhost:5173`.
6. Enter: `PostgreSQL connection refused on port 5432 after server restart`.
7. Click **Analyze Incident**.
8. Show the route: **Historical + Documentation**.
9. Show the category, severity, likely cause, and troubleshooting steps.
10. Open **Historical Incidents** and show the similar synthetic tickets.
11. Open **Documentation** and show the official PostgreSQL sources.

## Short Explanation

Say:

> The company uses GLPI for IT ticket management, but no internal company data was used in this prototype. I created a synthetic GLPI-inspired historical incident dataset and a small knowledge base from official public documentation.
>
> A small local Qwen model first decides whether the incident needs historical cases, documentation, both, or no retrieval. The query is embedded using BGE-small-en-v1.5 and searched using FAISS. Only sufficiently relevant results are kept.
>
> Those results are passed to a larger local Qwen model, which generates the diagnosis and troubleshooting steps. The historical tickets and documentation shown here are the actual evidence retrieved by the system.

## Secondary Demo: DNS

Enter:

```text
The workstation can ping 8.8.8.8 but cannot resolve domain names
```

Expected behavior:

- Route: **Historical + Documentation**
- Historical evidence includes DNS-related incidents.
- Documentation evidence includes DNS troubleshooting material.

## Direct Route Demo

Enter:

```text
What is localhost?
```

Explain:

> The router recognizes that this simple concept does not need retrieval, so it skips FAISS and sends no external evidence.

## Latency Note

The prototype runs entirely locally on a CPU-only laptop. RAG requests may take around 1–2 minutes when models are warm, and cold model startup may take longer. Retrieval itself takes less than one second; most latency comes from local 4B LLM inference. Run one request before the demonstration so the models are warm.

## Prototype Limitations

- Historical tickets are synthetic GLPI-style examples, not company records.
- The documentation corpus is intentionally small and focused.
- Similarity thresholds are simple prototype heuristics.
- The Qwen3 4B model runs locally on CPU and therefore has noticeable latency.
- The system provides evidence-backed assistance, not guaranteed root-cause confirmation.
- The frontend does not persist analysis history.
