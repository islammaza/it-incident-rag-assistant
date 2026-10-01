import { useEffect, useRef, useState } from "react";
import {
  ArrowRight,
  CheckCircle2,
  CircleAlert,
  ScanSearch,
  ShieldCheck,
} from "lucide-react";
import { Header } from "@/components/Header";
import { IncidentInput } from "@/components/IncidentInput";
import { AnalysisSummary } from "@/components/AnalysisSummary";
import { DiagnosisCard } from "@/components/DiagnosisCard";
import { TroubleshootingSteps } from "@/components/TroubleshootingSteps";
import { HistoricalEvidence } from "@/components/HistoricalEvidence";
import { DocumentationEvidence } from "@/components/DocumentationEvidence";
import { Tabs, TabsList, TabsTrigger, TabsContent } from "@/components/ui/tabs";
import { checkBackendHealth, diagnoseIncident } from "@/lib/api";
import type { DiagnoseResponse } from "@/types/diagnosis";

function App() {
  const [incident, setIncident] = useState("");
  const [result, setResult] = useState<DiagnoseResponse | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [backendOnline, setBackendOnline] = useState<boolean | null>(null);
  const resultHeading = useRef<HTMLHeadingElement>(null);

  useEffect(() => {
    checkBackendHealth().then(setBackendOnline);
  }, []);

  useEffect(() => {
    if (result) resultHeading.current?.focus({ preventScroll: true });
  }, [result]);

  async function analyze() {
    if (!incident.trim() || isLoading) return;
    setIsLoading(true);
    setError(null);
    try {
      setResult(await diagnoseIncident(incident.trim()));
    } catch {
      setResult(null);
      setError(
        "Unable to analyze the incident. Make sure the FastAPI backend and Ollama are running.",
      );
    } finally {
      setIsLoading(false);
    }
  }

  function changeIncident(value: string) {
    setIncident(value);
    setResult(null);
    setError(null);
  }

  function clearAnalysis() {
    setIncident("");
    setResult(null);
    setError(null);
  }

  return (
    <div className="min-h-screen">
      <a
        href="#main-content"
        className="sr-only fixed top-3 left-3 z-50 rounded-md bg-primary px-4 py-2 text-sm focus:not-sr-only"
      >
        Skip to main content
      </a>
      <Header backendOnline={backendOnline} />
      <main
        id="main-content"
        className="mx-auto max-w-7xl px-5 py-8 sm:px-8 sm:py-10"
      >
        <div className="mb-7 flex flex-wrap items-end justify-between gap-4">
          <div>
            <p className="eyebrow mb-2">Incident workspace</p>
            <h1 className="text-2xl font-semibold tracking-tight">
              Clarity for your next incident.
            </h1>
            <p className="mt-2 text-sm text-muted-foreground">
              Investigate the issue. Understand the evidence. Find your next
              step.
            </p>
          </div>
          <span className="flex items-center gap-1.5 rounded-md border border-border bg-secondary/30 px-2.5 py-1 text-[11px] text-slate-400">
            Local RAG workspace
          </span>
        </div>
        <IncidentInput
          incident={incident}
          loading={isLoading}
          onChange={changeIncident}
          onAnalyze={analyze}
        />
        <div role="status" aria-live="polite" className="sr-only">
          {isLoading
            ? "Analyzing incident..."
            : result
              ? "Analysis complete."
              : ""}
        </div>
        {error ? (
          <section
            className="mt-7 flex items-start gap-3 rounded-xl border border-red-400/25 bg-red-400/5 p-5"
            role="alert"
          >
            <CircleAlert className="mt-0.5 size-5 shrink-0 text-red-300" />
            <div className="min-w-0">
              <h2 className="text-sm font-semibold text-red-200">
                Analysis unavailable
              </h2>
              <p className="mt-1 text-sm leading-6 text-red-100/70">{error}</p>
              <button
                type="button"
                onClick={analyze}
                className="mt-3 text-xs font-medium text-red-200 underline underline-offset-4"
              >
                Try Again
              </button>
            </div>
          </section>
        ) : !result ? (
          <section
            aria-label="Analysis preview"
            aria-busy={isLoading}
            className="mt-7 flex flex-col items-center rounded-xl border border-dashed border-slate-700/70 px-5 py-9 text-center"
          >
            <ScanSearch className="mb-3 size-7 text-slate-500" />
            <h2 className="text-sm font-medium text-slate-300">
              {isLoading
                ? "Analyzing incident..."
                : "Your investigation starts here"}
            </h2>
            <p className="mt-2 max-w-md text-xs leading-6 text-muted-foreground">
              {isLoading
                ? "Routing the request, retrieving evidence, and generating a grounded diagnosis..."
                : "Describe an incident above to receive a structured diagnosis, troubleshooting steps, and supporting sources."}
            </p>
            <div className="mt-5 flex flex-wrap items-center justify-center gap-2 text-[11px] text-slate-400">
              <span>Route</span>
              <ArrowRight className="size-3 text-slate-600" />
              <span>Retrieve</span>
              <ArrowRight className="size-3 text-slate-600" />
              <span>Analyze</span>
            </div>
          </section>
        ) : (
          <section className="mt-10 space-y-5" aria-labelledby="result-heading">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <div>
                <div className="flex flex-wrap items-center gap-3">
                  <h2
                    ref={resultHeading}
                    tabIndex={-1}
                    id="result-heading"
                    className="rounded-sm text-lg font-semibold"
                  >
                    Analysis Result
                  </h2>
                  <span className="flex items-center gap-1.5 text-xs text-emerald-300">
                    <CheckCircle2 className="size-3.5" />
                    Analysis complete
                  </span>
                </div>
                <p className="mt-2 text-xs text-muted-foreground">
                  Real local RAG response · Retrieved evidence is shown below
                </p>
              </div>
              <button
                type="button"
                onClick={clearAnalysis}
                className="text-xs text-muted-foreground underline underline-offset-4 hover:text-foreground"
              >
                New Analysis
              </button>
            </div>
            <AnalysisSummary result={result} />
            <DiagnosisCard diagnosis={result.diagnosis} />
            <div className="grid items-start gap-6 lg:grid-cols-[.85fr_1.15fr]">
              <TroubleshootingSteps
                steps={result.diagnosis.troubleshooting_steps}
              />
              <section aria-labelledby="evidence-heading" className="min-w-0">
                <div className="mb-4 flex gap-3">
                  <ShieldCheck className="section-icon" />
                  <div>
                    <h3
                      id="evidence-heading"
                      className="text-base font-semibold"
                    >
                      Evidence used for this analysis
                    </h3>
                    <p className="mt-1 text-xs leading-6 text-muted-foreground">
                      Historical causes and resolutions are evidence, not
                      confirmed facts about the current incident.
                    </p>
                  </div>
                </div>
                {result.historical_incidents.length === 0 &&
                result.documentation.length === 0 ? (
                  <p className="rounded-lg border border-border/70 bg-card p-5 text-sm text-muted-foreground">
                    Direct analysis · No external evidence was retrieved for
                    this query.
                  </p>
                ) : (
                  <Tabs
                    defaultValue={
                      result.historical_incidents.length
                        ? "historical"
                        : "documentation"
                    }
                    className="gap-4"
                  >
                    <TabsList
                      className={`grid h-auto w-full p-1 ${result.historical_incidents.length && result.documentation.length ? "grid-cols-2" : "grid-cols-1"}`}
                    >
                      {result.historical_incidents.length > 0 && (
                        <TabsTrigger
                          value="historical"
                          className="min-w-0 whitespace-normal px-2 py-2 text-xs"
                        >
                          Historical Incidents (
                          {result.historical_incidents.length})
                        </TabsTrigger>
                      )}
                      {result.documentation.length > 0 && (
                        <TabsTrigger
                          value="documentation"
                          className="min-w-0 whitespace-normal px-2 py-2 text-xs"
                        >
                          Documentation ({result.documentation.length})
                        </TabsTrigger>
                      )}
                    </TabsList>
                    {result.historical_incidents.length > 0 && (
                      <TabsContent value="historical">
                        <HistoricalEvidence
                          incidents={result.historical_incidents}
                        />
                      </TabsContent>
                    )}
                    {result.documentation.length > 0 && (
                      <TabsContent value="documentation">
                        <DocumentationEvidence sources={result.documentation} />
                      </TabsContent>
                    )}
                  </Tabs>
                )}
              </section>
            </div>
          </section>
        )}
        <footer className="mt-8 flex flex-wrap items-center justify-between gap-2 border-t border-border/60 pt-5 text-[11px] text-slate-500">
          <span>
            IncidentIQ <span className="mx-2">/</span> Evidence-backed incident
            analysis
          </span>
          <span>Local AI · FastAPI + LangGraph</span>
        </footer>
      </main>
    </div>
  );
}

export default App;
