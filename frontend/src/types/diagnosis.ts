export interface Diagnosis {
  category: string;
  severity: "Low" | "Medium" | "High" | "Critical";
  likely_cause: string;
  explanation: string;
  troubleshooting_steps: string[];
}

export interface HistoricalIncident {
  ticket_id: string;
  title: string;
  category?: string | null;
  score: number;
  root_cause?: string | null;
  solution?: string | null;
}

export interface DocumentationSource {
  title: string;
  source: string;
  url: string;
  product?: string | null;
  topic?: string | null;
  score: number;
}

export interface DiagnoseResponse {
  route: "historical" | "documentation" | "both" | "direct";
  diagnosis: Diagnosis;
  historical_incidents: HistoricalIncident[];
  documentation: DocumentationSource[];
}
