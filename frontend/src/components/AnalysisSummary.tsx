import { BookOpen, GitBranch, Layers3 } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card } from "@/components/ui/card";
import type { DiagnoseResponse, Diagnosis } from "@/types/diagnosis";

const routeLabels: Record<DiagnoseResponse["route"], string> = {
  historical: "Historical Incidents",
  documentation: "Documentation",
  both: "Historical + Documentation",
  direct: "Direct Analysis",
};
const severityStyles: Record<Diagnosis["severity"], string> = {
  Low: "border-emerald-400/25 bg-emerald-400/10 text-emerald-300",
  Medium: "border-amber-400/25 bg-amber-400/10 text-amber-300",
  High: "border-orange-400/30 bg-orange-400/10 text-orange-300",
  Critical: "border-red-400/40 bg-red-500/20 text-red-200",
};
export function AnalysisSummary({ result }: { result: DiagnoseResponse }) {
  return (
    <Card className="grid gap-0 overflow-hidden py-0 sm:grid-cols-2 xl:grid-cols-[1.3fr_1.1fr_.7fr_.7fr]">
      <div className="p-5">
        <p className="eyebrow">Retrieval route</p>
        <p className="mt-3 flex items-center gap-2 text-sm">
          <GitBranch className="size-4 shrink-0 text-blue-400" />
          {routeLabels[result.route]}
        </p>
      </div>
      <div className="border-t p-5 sm:border-t-0 sm:border-l">
        <p className="eyebrow">Category</p>
        <p className="mt-3 flex items-center gap-2 text-sm">
          <Layers3 className="size-4 shrink-0 text-muted-foreground" />
          {result.diagnosis.category}
        </p>
      </div>
      <div className="border-t p-5 xl:border-t-0 xl:border-l">
        <p className="eyebrow">Severity</p>
        <Badge
          variant="outline"
          className={`mt-2 ${severityStyles[result.diagnosis.severity]}`}
        >
          <span className="mr-1 size-1.5 rounded-full bg-current" />
          {result.diagnosis.severity}
        </Badge>
      </div>
      <div className="border-t p-5 sm:border-l xl:border-t-0">
        <p className="eyebrow">Retrieved evidence</p>
        <p className="mt-3 flex items-center gap-2 text-sm">
          <BookOpen className="size-4 text-muted-foreground" />
          {result.historical_incidents.length +
            result.documentation.length}{" "}
          sources
        </p>
      </div>
    </Card>
  );
}
