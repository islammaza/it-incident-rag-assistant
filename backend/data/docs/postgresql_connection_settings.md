---
title: PostgreSQL Connection Settings
source: PostgreSQL Documentation
url: https://www.postgresql.org/docs/current/libpq-connect.html
product: PostgreSQL
topic: Connections
---

# PostgreSQL Connection Settings

PostgreSQL clients can specify a connection with a keyword/value string, a URI, or separate parameters. The commonly relevant settings are `host`, `port`, `dbname`, `user`, and authentication-related options. The default PostgreSQL port is `5432`; a non-default port must be supplied by the client and by the server configuration.

## Troubleshooting checklist

1. Confirm the database hostname resolves to the expected private address.
2. Test whether the host accepts TCP connections on the configured port.
3. Confirm the client and server use the same database name and user.
4. Check whether the server is listening on the requested address and port.
5. Review the server log for connection, startup, or authentication messages.

A connection refusal usually means that no process is accepting connections at the target address and port, or that a firewall is rejecting the connection. A timeout can indicate a routing or firewall problem. If the TCP connection succeeds but PostgreSQL rejects the client, inspect authentication rules and the database logs.

Connection settings should be kept separate from application code where possible. Do not place passwords or other secrets in this knowledge base. When diagnosing an incident, record the non-sensitive host, port, database, and observed error, then verify the result with a small application health check.
