---
title: Windows DNS Troubleshooting
source: Microsoft Learn
url: https://learn.microsoft.com/en-us/windows-server/networking/dns/troubleshoot/troubleshoot-dns-data-collection
product: Windows
topic: DNS Troubleshooting
---

# Windows DNS Troubleshooting

Windows DNS incidents should be investigated from the affected client and compared with a known-good system. `ipconfig /all` identifies configured DNS servers. `nslookup name` performs a direct lookup and shows which server answered. PowerShell's `Resolve-DnsName name` provides structured query details for supported records.

Check whether the result is an address, `NXDOMAIN`, a timeout, or a server failure. Confirm that the client is querying the intended internal resolver and that the resolver can reach authoritative sources. A stale client cache can preserve an old result, but clearing it should follow correction of the record or resolver path rather than replace that diagnosis.

## Troubleshooting sequence

- Record the exact name and record type being queried.
- Compare results from the affected and known-good clients.
- Check DNS server addresses and network reachability.
- Query the intended server directly when permitted.
- Review recent DNS record, DHCP, VPN, or network profile changes.
- Retest the application hostname after the DNS issue is corrected.

Keep diagnostic outputs limited to synthetic or non-sensitive names in shared notes. DNS success proves name resolution only; test the resulting service address and port separately.
