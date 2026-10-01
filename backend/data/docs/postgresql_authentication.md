---
title: PostgreSQL Client Authentication
source: PostgreSQL Documentation
url: https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
product: PostgreSQL
topic: Authentication
---

# PostgreSQL Client Authentication

PostgreSQL controls client authentication with `pg_hba.conf`. Each record describes a connection type, database, user, client address or network, and authentication method. PostgreSQL checks records in order, so the first matching record determines the result. A later, more specific rule does not override an earlier matching rule.

For TCP connections, `host` records are used. The client address must match the address or network in the rule. A connection can therefore reach port `5432` successfully and still fail because the client subnet, database, or user is not allowed. Common messages include `no pg_hba.conf entry` and password authentication failures.

## Troubleshooting checklist

- Confirm the actual client IP or subnet.
- Confirm the requested database and user.
- Inspect the applicable `pg_hba.conf` entries in order.
- Check the configured authentication method and server logs.
- Reload PostgreSQL after an approved configuration change.

Use the PostgreSQL configuration view or the server's documented configuration path to confirm which file is active. Avoid broad access rules when a narrower approved network is sufficient. After changing authentication rules, test the exact application connection and verify that unrelated access was not widened.
