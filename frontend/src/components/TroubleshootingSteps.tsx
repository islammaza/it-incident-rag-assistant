import { ListChecks } from "lucide-react";
import { Card } from "@/components/ui/card";

export function TroubleshootingSteps({ steps }: { steps: string[] }) {
  if (steps.length === 0) return null;

  return (
    <Card className="gap-0 py-0">
      <div className="flex items-center gap-3 border-b p-5">
        <ListChecks className="section-icon" />
        <div>
          <h3 className="text-base font-semibold">Troubleshooting steps</h3>
          <p className="mt-1 text-xs text-muted-foreground">
            A practical path to verification
          </p>
        </div>
      </div>
      <ol className="divide-y divide-border/70 px-5">
        {steps.map((step, index) => (
          <li key={step} className="flex gap-3 py-5">
            <span className="flex size-6 shrink-0 items-center justify-center rounded-full border border-slate-600/50 bg-secondary text-[11px] font-medium text-slate-300">
              {String(index + 1).padStart(2, "0")}
            </span>
            <p className="text-sm leading-6 text-slate-300">{step}</p>
          </li>
        ))}
      </ol>
    </Card>
  );
}
