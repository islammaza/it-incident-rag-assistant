---
title: PostgreSQL Server Startup Troubleshooting
source: PostgreSQL Documentation
url: https://www.postgresql.org/docs/current/server-start.html
product: PostgreSQL
topic: Server Startup
---

# PostgreSQL Server Startup Troubleshooting

When PostgreSQL does not accept connections, first determine whether the server process is running and whether it completed startup. On a Linux installation managed by systemd, inspect the service status and journal. PostgreSQL logs commonly identify invalid configuration, missing directories, unavailable filesystems, port conflicts, or recovery in progress.

A service can be active while the database is still starting or while it listens on a different address than the client expects. Check the configured port and `listen_addresses`, then confirm the listening socket with an operating-system tool. A connection refusal means the requested socket is not accepting connections; it does not by itself identify whether the cause is a stopped service, wrong address, port conflict, or firewall.

## Safe diagnostic sequence

1. Check service status and recent startup logs.
2. Validate the PostgreSQL configuration before reloading or restarting.
3. Confirm the data directory and required filesystem are mounted and writable.
4. Check for another process using the expected port.
5. Confirm the server is listening on the expected address and port.
6. Test a local connection, then an approved application connection.

Do not repeatedly restart a database without reviewing logs. If recovery is active after an unclean shutdown, allow it to complete unless the documented operational procedure says otherwise.
