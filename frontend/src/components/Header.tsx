import { Activity, Cpu } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export function Header({ backendOnline }: { backendOnline: boolean | null }) {
  const statusLabel =
    backendOnline === null
      ? "Checking backend"
      : backendOnline
        ? "Backend Online"
        : "Backend Offline";
  const statusClass =
    backendOnline === false
      ? "border-red-400/20 bg-red-400/5 text-red-300"
      : "border-emerald-400/20 bg-emerald-400/5 text-emerald-300";

  return (
    <header className="border-b border-border/80 bg-background/95">
      <div className="mx-auto flex max-w-7xl flex-wrap items-center justify-between gap-4 px-5 py-5 sm:px-8">
        <div className="flex items-center gap-3">
          <div className="flex size-10 items-center justify-center rounded-xl border border-blue-400/25 bg-blue-500/10 text-blue-400">
            <Activity className="size-6" />
          </div>
          <div>
            <p className="text-lg font-semibold tracking-tight">
              Incident<span className="text-blue-400">IQ</span>
            </p>
            <p className="text-xs text-muted-foreground">
              AI-assisted incident diagnosis
            </p>
          </div>
        </div>
        <div className="flex items-center gap-3">
          <span className="hidden items-center gap-2 text-xs text-muted-foreground sm:flex">
            <Cpu className="size-3.5" /> Local AI · RAG
          </span>
          <Badge variant="outline" className={`gap-2 px-3 py-1 ${statusClass}`}>
            <span
              className={`size-1.5 rounded-full ${backendOnline === false ? "bg-red-400" : "bg-emerald-400"}`}
            />
            {statusLabel}
          </Badge>
        </div>
      </div>
    </header>
  );
}
