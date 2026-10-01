from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .graph import run_incident_analysis
from .schemas import DiagnoseRequest, DiagnoseResponse

app = FastAPI(title="IT Incident RAG Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/api/diagnose", response_model=DiagnoseResponse)
def diagnose(request: DiagnoseRequest) -> DiagnoseResponse:
    try:
        result = run_incident_analysis(request.incident)
        historical_incidents = [
            {
                "ticket_id": incident["ticket_id"],
                "title": incident["title"],
                "category": incident.get("category"),
                "score": incident["score"],
                "root_cause": incident.get("root_cause"),
                "solution": incident.get("solution"),
            }
            for incident in result.get("retrieved_incidents", [])
        ]
        documentation = [
            {
                "title": document["title"],
                "source": document["source"],
                "url": document["url"],
                "product": document.get("product"),
                "topic": document.get("topic"),
                "score": document["score"],
            }
            for document in result.get("retrieved_docs", [])
        ]
        return DiagnoseResponse(
            route=result["route"],
            diagnosis=result["diagnosis"],
            historical_incidents=historical_incidents,
            documentation=documentation,
        )
    except Exception as error:
        raise HTTPException(status_code=500, detail="Diagnosis pipeline failed.") from error
