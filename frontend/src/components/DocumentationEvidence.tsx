import { BookOpen, ExternalLink } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import type { DocumentationSource } from "@/types/diagnosis";

export function DocumentationEvidence({
  sources,
}: {
  sources: DocumentationSource[];
}) {
  return (
    <div className="space-y-3">
      <p className="px-1 text-xs leading-5 text-muted-foreground">
        Official technical documentation · Sample sources from the project
        knowledge base.
      </p>
      {sources.map((source) => (
        <article
          key={source.url}
          className="rounded-xl border bg-card p-4 sm:p-5"
        >
          <div className="flex gap-3">
            <BookOpen className="mt-1 size-4 shrink-0 text-blue-300" />
            <div className="min-w-0">
              <h4 className="text-sm font-semibold leading-6">
                {source.title}
              </h4>
              <p className="mt-1 text-xs text-muted-foreground">
                {source.source}
              </p>
              <p className="mt-2 text-xs text-slate-400">
                {source.product} · {source.topic}
              </p>
            </div>
          </div>
          <div className="mt-4 flex flex-wrap items-center justify-between gap-3 border-t border-border/70 pt-3">
            <Badge
              variant="outline"
              className="border-slate-600/50 text-[10px] font-normal text-slate-300"
            >
              Similarity {Math.round(source.score * 100)}%
            </Badge>
            <a
              href={source.url}
              target="_blank"
              rel="noreferrer"
              aria-label={`Open Source: ${source.title} (opens in a new tab)`}
              className="inline-flex items-center gap-1.5 rounded-sm text-xs font-medium text-blue-300 hover:text-blue-200"
            >
              Open Source
              <ExternalLink className="size-3" />
            </a>
          </div>
        </article>
      ))}
    </div>
  );
}
