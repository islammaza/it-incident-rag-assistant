import { ScanSearch } from "lucide-react";
import { Card } from "@/components/ui/card";
import type { Diagnosis } from "@/types/diagnosis";

export function DiagnosisCard({ diagnosis }: { diagnosis: Diagnosis }) {
  return (
    <Card className="gap-0 overflow-hidden py-0">
      <div className="border-b border-border bg-blue-500/[0.035] p-5 sm:p-6">
        <div className="mb-4 flex items-center gap-2 text-blue-300">
          <ScanSearch className="size-4" />
          <h3 className="text-sm font-semibold">Likely Cause</h3>
        </div>
        <p className="max-w-4xl text-lg font-medium leading-8 tracking-tight">
          {diagnosis.likely_cause}
        </p>
        <p className="mt-3 text-xs leading-5 text-muted-foreground">
          AI-generated assessment based on retrieved evidence
        </p>
      </div>
      <div className="p-5 sm:p-6">
        <h3 className="mb-3 text-sm font-semibold">Explanation</h3>
        <p className="max-w-5xl text-sm leading-7 text-slate-300">
          {diagnosis.explanation}
        </p>
      </div>
    </Card>
  );
}
