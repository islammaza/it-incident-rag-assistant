---
title: DNS Resolution Troubleshooting
source: Ubuntu Documentation
url: https://documentation.ubuntu.com/server/how-to/networking/install-dns/
product: DNS / Networking
topic: DNS Resolution
---

# DNS Resolution Troubleshooting

DNS translates hostnames into addresses and can fail even when direct IP connectivity works. Separate name resolution from network reachability: first query the name, then test the resulting address and service port. Useful local commands include `resolvectl status`, `resolvectl query name`, `getent hosts name`, and `dig name` when available.

Check which resolver is configured, whether it is reachable, and whether the requested name belongs to the expected internal zone. Common observations include `NXDOMAIN` for a name that does not exist, `SERVFAIL` for an authoritative or recursive failure, and timeouts when the resolver cannot be reached or does not respond in time.

## Troubleshooting sequence

1. Confirm the exact hostname, search domain, and expected address.
2. Inspect active resolver configuration.
3. Query the name from the affected host and a known-good host.
4. Test resolver connectivity and the returned address separately.
5. Check recent DNS records, network changes, and resolver logs.
6. Flush a local cache only after correcting the underlying record or resolver issue.

Do not replace an internal hostname with an IP as a permanent fix without understanding the service dependency. Record the query result and resolver used, but do not include confidential domain data in this public synthetic knowledge base.
