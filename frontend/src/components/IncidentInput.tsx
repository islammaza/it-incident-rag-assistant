import {
  ArrowRight,
  Database,
  FileText,
  Loader2,
  Terminal,
} from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card } from "@/components/ui/card";
import { Textarea } from "@/components/ui/textarea";
import { examples } from "@/data/mockData";

interface Props {
  incident: string;
  loading: boolean;
  onChange: (value: string) => void;
  onAnalyze: () => void;
}

export function IncidentInput({
  incident,
  loading,
  onChange,
  onAnalyze,
}: Props) {
  return (
    <Card className="gap-0 overflow-hidden border-slate-700/80 py-0 shadow-xl shadow-black/10">
      <div className="grid lg:grid-cols-[1fr_280px]">
        <form
          className="min-w-0 p-5 sm:p-7"
          onSubmit={(event) => {
            event.preventDefault();
            onAnalyze();
          }}
        >
          <div className="mb-5 flex items-center gap-3">
            <Terminal className="section-icon" />
            <div>
              <h2 className="text-lg font-semibold">Analyze an IT Incident</h2>
              <p className="mt-1 text-sm text-muted-foreground">
                Describe the issue, paste an error message, or include a short
                log extract.
              </p>
            </div>
          </div>
          <label
            htmlFor="incident"
            className="mb-2 block text-xs font-medium text-slate-300"
          >
            Incident description
          </label>
          <Textarea
            id="incident"
            value={incident}
            disabled={loading}
            onChange={(event) => onChange(event.target.value)}
            rows={6}
            placeholder="Example: PostgreSQL connection refused on port 5432 after server restart..."
            aria-describedby="demo-note"
            className="min-h-40 resize-y rounded-lg border-slate-700 bg-background/70 px-4 py-3 font-mono text-sm leading-7 placeholder:text-slate-500 focus-visible:border-blue-400"
          />
          <div className="mt-3 flex flex-wrap items-center gap-2">
            <span className="mr-1 text-xs text-muted-foreground">
              Try an example
            </span>
            {examples.map((example) => (
              <Button
                key={example.label}
                type="button"
                variant="outline"
                size="sm"
                disabled={loading}
                aria-pressed={incident === example.text}
                onClick={() => onChange(example.text)}
                className="h-7 rounded-md border-border bg-secondary/35 px-2.5 text-[11px] text-slate-300 aria-pressed:border-blue-400/50 aria-pressed:bg-blue-500/10 aria-pressed:text-blue-300"
              >
                {example.label}
              </Button>
            ))}
          </div>
          <div className="mt-6 flex flex-col gap-4 border-t border-border/70 pt-5 sm:flex-row sm:items-center sm:justify-between">
            <p
              id="demo-note"
              className="max-w-sm text-xs leading-5 text-muted-foreground"
            >
              Local AI · Requests are sent to the local FastAPI diagnosis
              endpoint.
            </p>
            <Button
              type="submit"
              disabled={!incident.trim() || loading}
              className="shrink-0 gap-2 px-5 shadow-md shadow-blue-950/30"
            >
              {loading ? (
                <>
                  <Loader2 className="size-4 motion-safe:animate-spin" />
                  Analyzing...
                </>
              ) : (
                <>
                  Analyze Incident
                  <ArrowRight className="size-4" />
                </>
              )}
            </Button>
          </div>
        </form>
        <aside className="border-t border-border/70 bg-background/25 p-5 sm:p-7 lg:border-t-0 lg:border-l">
          <p className="eyebrow mb-5">Context before conclusions</p>
          <h3 className="text-base font-medium leading-6">
            From incident to
            <br className="hidden lg:block" /> informed next steps.
          </h3>
          <p className="mt-3 text-sm leading-6 text-muted-foreground">
            Bring historical experience and technical documentation into one
            investigation.
          </p>
          <div className="mt-6 space-y-5">
            <div className="flex gap-3">
              <Database className="mt-0.5 size-4 shrink-0 text-blue-400" />
              <div>
                <p className="text-xs font-medium">Historical incidents</p>
                <p className="mt-1 text-xs leading-5 text-muted-foreground">
                  Similar issues and past resolutions
                </p>
              </div>
            </div>
            <div className="flex gap-3">
              <FileText className="mt-0.5 size-4 shrink-0 text-blue-400" />
              <div>
                <p className="text-xs font-medium">Technical documentation</p>
                <p className="mt-1 text-xs leading-5 text-muted-foreground">
                  Source-linked troubleshooting context
                </p>
              </div>
            </div>
          </div>
        </aside>
      </div>
    </Card>
  );
}
