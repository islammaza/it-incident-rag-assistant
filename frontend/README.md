# IncidentIQ frontend

Step 13: a responsive, local UI demonstration for the IT Incident RAG Assistant. No backend integration, authentication, routing, analytics, or deployment is included.

## Run

From this folder:

```sh
npm install
npm run dev
```

Open http://localhost:5173. On Windows PowerShell, use `npm.cmd install` and `npm.cmd run dev` if execution policy blocks `npm.ps1`.

```sh
npm run build
npm run lint
npm run preview
```

## Structure

```text
frontend/
  src/
    components/
      Header.tsx
      IncidentInput.tsx
      AnalysisSummary.tsx
      DiagnosisCard.tsx
      TroubleshootingSteps.tsx
      HistoricalEvidence.tsx
      DocumentationEvidence.tsx
      ui/                     # shadcn button, badge, card, tabs, textarea
    data/mockData.ts          # Response interfaces, example incidents, static result
    lib/utils.ts              # shadcn class-name helper
    App.tsx                   # Local state and page layout
    main.tsx
    index.css                 # Tailwind and dark theme
  screenshots/                # Desktop and mobile browser captures
  components.json
  vite.config.ts
  tsconfig*.json
  package.json
  package-lock.json
  index.html
```

## Stack

React, React DOM, TypeScript, Vite, Tailwind CSS with its Vite plugin, shadcn/ui, and Lucide React. The shadcn components use Radix Slot and Tabs, class-variance-authority, clsx, and tailwind-merge. Oxlint is supplied by the Vite starter. Playwright was used temporarily for browser verification and is not a project dependency.

Setup references: [Vite](https://vite.dev/guide/) and [shadcn/ui for Vite](https://ui.shadcn.com/docs/installation/vite).

## Demo behavior

- Results start hidden. Empty or whitespace-only input disables Analyze Incident.
- Each example chip replaces the textarea with a realistic incident description.
- Analyze shows a disabled button with a spinner for 650 ms, then displays the same PostgreSQL sample for every input. The UI explicitly labels this behavior.
- Editing the incident hides the old result. The timeout is cleaned up on unmount.
- The mock response mirrors the backend field names. Historical ticket details and documentation metadata come from the existing project dataset; similarity values and the diagnosis are illustrative.
- Results show the route, category, severity, seven evidence sources, likely cause, explanation, and five troubleshooting steps.
- Historical Incidents (3) and Documentation (4) are accessible Radix tabs. Arrow keys switch between tabs. Source links open in a new tab.
- Route labels cover historical, documentation, both, and direct. Severity styling covers Low, Medium, High, and Critical; the sample is Medium in amber.
- Desktop uses columns; smaller screens stack the cards. Focus indicators, a skip link, textarea labeling, live status announcements, and reduced-motion support are included.
- There is no fetch, Axios, API URL, or FastAPI connection. Clicking a documentation link intentionally opens the external official source.

## Verification

Production build and lint pass. Browser checks covered empty and whitespace input, all chips, loading, sample rendering, result reset, both evidence tabs, keyboard tab navigation, and source-link attributes. Responsive overflow checks passed at 320, 390, 768, 1280, and 1440 pixels. Desktop and mobile screenshots were visually inspected. No runtime errors or fetch/XHR requests were observed.
