import { History } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { HistoricalIncident } from "@/types/diagnosis";

export function HistoricalEvidence({
  incidents,
}: {
  incidents: HistoricalIncident[];
}) {
  return (
    <div className="space-y-3">
      <p className="px-1 text-xs leading-5 text-muted-foreground">
        Similar historical tickets · Past causes and resolutions, not confirmed
        facts about this incident.
      </p>
      {incidents.map((incident) => (
        <article
          key={incident.ticket_id}
          className="rounded-xl border bg-card p-4 sm:p-5"
        >
          <div className="mb-3 flex flex-wrap items-center justify-between gap-2">
            <span className="flex items-center gap-2 font-mono text-xs text-blue-300">
              <History className="size-3.5" />
              {incident.ticket_id}
            </span>
            <Badge
              variant="outline"
              className="border-slate-600/50 text-[10px] font-normal text-slate-300"
            >
              Similarity {Math.round(incident.score * 100)}%
            </Badge>
          </div>
          <h4 className="text-sm font-semibold leading-6">{incident.title}</h4>
          <p className="mt-1 text-xs text-muted-foreground">
            {incident.category}
          </p>
          <dl className="mt-4 space-y-3 border-t border-border/70 pt-4 text-xs leading-5">
            <div>
              <dt className="mb-1 font-medium text-slate-300">
                Historical cause
              </dt>
              <dd className="text-muted-foreground">{incident.root_cause}</dd>
            </div>
            <div>
              <dt className="mb-1 font-medium text-slate-300">
                Historical resolution
              </dt>
              <dd className="text-muted-foreground">{incident.solution}</dd>
            </div>
          </dl>
        </article>
      ))}
    </div>
  );
}
