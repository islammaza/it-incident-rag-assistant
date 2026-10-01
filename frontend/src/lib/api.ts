import type { DiagnoseResponse } from "@/types/diagnosis";

const API_BASE_URL = "http://127.0.0.1:8000";

export async function diagnoseIncident(
  incident: string,
): Promise<DiagnoseResponse> {
  const response = await fetch(`${API_BASE_URL}/api/diagnose`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ incident }),
  });

  if (!response.ok) {
    throw new Error("Unable to analyze the incident.");
  }

  return response.json() as Promise<DiagnoseResponse>;
}

export async function checkBackendHealth(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    return response.ok;
  } catch {
    return false;
  }
}
