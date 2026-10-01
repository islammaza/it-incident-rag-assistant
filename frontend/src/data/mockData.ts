export interface Diagnosis {
  category: string;
  severity: "Low" | "Medium" | "High" | "Critical";
  likely_cause: string;
  explanation: string;
  troubleshooting_steps: string[];
}
export interface HistoricalIncident {
  ticket_id: string;
  title: string;
  category: string;
  score: number;
  root_cause: string;
  solution: string;
}
export interface DocumentationSource {
  title: string;
  source: string;
  url: string;
  product: string;
  topic: string;
  score: number;
}
export interface AnalysisResult {
  route: "historical" | "documentation" | "both" | "direct";
  diagnosis: Diagnosis;
  historical_incidents: HistoricalIncident[];
  documentation: DocumentationSource[];
}

export const examples = [
  {
    label: "PostgreSQL",
    text: "PostgreSQL connection refused on port 5432 after server restart",
  },
  {
    label: "Nginx 502",
    text: "Nginx returns 502 Bad Gateway after deploying the application. The upstream service is not responding.",
  },
  {
    label: "DNS Failure",
    text: "Internal service hostnames cannot be resolved, but connections using IP addresses still work.",
  },
  {
    label: "Docker Restart",
    text: "A Docker container keeps restarting after deployment. Logs show that the application exits during startup.",
  },
  {
    label: "Disk Full",
    text: "The Linux server reports No space left on device. Application writes are failing on the root filesystem.",
  },
  {
    label: "What is localhost?",
    text: "What is localhost?",
  },
];

// Static demonstration only. Every incident displays this same PostgreSQL sample.
export const mockAnalysis: AnalysisResult = {
  route: "both",
  diagnosis: {
    category: "Database / PostgreSQL",
    severity: "Medium",
    likely_cause:
      "PostgreSQL likely failed to start correctly after the server restart.",
    explanation:
      "The application cannot establish a TCP connection to PostgreSQL on port 5432. A connection-refused error is consistent with a service that is stopped or not listening on the expected address. Similar historical incidents point to startup configuration errors or a disabled service. Check the service and its startup logs to confirm the cause before making changes.",
    troubleshooting_steps: [
      "Check PostgreSQL service status to verify whether the service is active, stopped, or failed.",
      "Inspect PostgreSQL startup logs and systemd journal entries for configuration errors.",
      "Verify that port 5432 and the listen_addresses setting match the expected server configuration.",
      "Check that the PostgreSQL data directory exists and has the correct ownership and permissions.",
      "Test local connectivity, then confirm that the application can connect to the database.",
    ],
  },
  historical_incidents: [
    {
      ticket_id: "INC-0001",
      title: "PostgreSQL unavailable after Linux server restart",
      category: "Database / PostgreSQL",
      score: 0.8742,
      root_cause:
        "An invalid PostgreSQL configuration prevented the database service from starting.",
      solution:
        "Corrected the configuration, restarted PostgreSQL, verified port 5432, and tested application connectivity.",
    },
    {
      ticket_id: "INC-0002",
      title: "Application connection refused on PostgreSQL port",
      category: "Database / PostgreSQL",
      score: 0.8321,
      root_cause:
        "The PostgreSQL service was disabled during a package maintenance operation.",
      solution:
        "Enabled and started the PostgreSQL service, then reran the application database health check.",
    },
    {
      ticket_id: "INC-0003",
      title: "Database service failed after configuration change",
      category: "Database / PostgreSQL",
      score: 0.7918,
      root_cause:
        "The configured listen address was invalid for the database host.",
      solution:
        "Restored a valid listen address, started the service, and verified local and application connections.",
    },
  ],
  documentation: [
    {
      title: "PostgreSQL Server Startup Troubleshooting",
      source: "PostgreSQL Documentation",
      url: "https://www.postgresql.org/docs/current/server-start.html",
      product: "PostgreSQL",
      topic: "Server Startup",
      score: 0.7941,
    },
    {
      title: "PostgreSQL Connection Settings",
      source: "PostgreSQL Documentation",
      url: "https://www.postgresql.org/docs/current/libpq-connect.html",
      product: "PostgreSQL",
      topic: "Connections",
      score: 0.7628,
    },
    {
      title: "Linux systemd Service Troubleshooting",
      source: "Ubuntu Documentation",
      url: "https://documentation.ubuntu.com/server/explanation/systemd/service-management/",
      product: "Linux / Ubuntu",
      topic: "systemd Services",
      score: 0.7412,
    },
    {
      title: "Linux File Permissions Troubleshooting",
      source: "Ubuntu Documentation",
      url: "https://documentation.ubuntu.com/desktop/en/latest/tutorial/file-permissions/",
      product: "Linux / Ubuntu",
      topic: "File Permissions",
      score: 0.7023,
    },
  ],
};
