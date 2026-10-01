from typing import Literal

from pydantic import BaseModel, field_validator


class DiagnosisResult(BaseModel):
    category: str
    severity: Literal["Low", "Medium", "High", "Critical"]
    likely_cause: str
    explanation: str
    troubleshooting_steps: list[str]


class DiagnoseRequest(BaseModel):
    incident: str

    @field_validator("incident")
    @classmethod
    def validate_incident(cls, value: str) -> str:
        cleaned_value = value.strip()
        if len(cleaned_value) < 3:
            raise ValueError("incident must contain at least 3 characters")
        return cleaned_value


class HistoricalEvidence(BaseModel):
    ticket_id: str
    title: str
    category: str | None = None
    score: float
    root_cause: str | None = None
    solution: str | None = None


class DocumentationEvidence(BaseModel):
    title: str
    source: str
    url: str
    product: str | None = None
    topic: str | None = None
    score: float


class DiagnoseResponse(BaseModel):
    route: str
    diagnosis: DiagnosisResult
    historical_incidents: list[HistoricalEvidence]
    documentation: list[DocumentationEvidence]
