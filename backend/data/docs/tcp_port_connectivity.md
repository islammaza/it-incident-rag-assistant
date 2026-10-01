---
title: TCP Port Connectivity Troubleshooting
source: Microsoft Learn
url: https://learn.microsoft.com/en-us/powershell/module/nettcpip/test-netconnection
product: DNS / Networking
topic: TCP Connectivity and Ports
---

# TCP Port Connectivity Troubleshooting

A service can have a resolvable hostname and a reachable host while its application port remains unavailable. Test the layers separately: resolve the name, reach the address, and then test the target TCP port. On Windows, `Test-NetConnection host -Port 5432` reports TCP connectivity. On Linux, an approved equivalent such as `nc -vz host 5432` or a client-specific connection test can check the port.

A successful ping does not prove that a TCP service is available; ICMP and TCP are separate protocols. `Connection refused` generally means the target host actively rejected the connection or no process is listening. A timeout may indicate filtering, routing failure, an unavailable host, or a service that is not responding.

## Diagnostic sequence

1. Confirm the hostname resolves to the expected private address.
2. Test the exact port from the same network location as the application.
3. Check the server process and listening socket.
4. Review host and network firewall rules for the source and destination.
5. Compare with a known-good client or subnet.
6. Retest the application protocol after correcting the failing layer.

Use the smallest approved test and avoid scanning unrelated ports. Keep private addresses and service names synthetic in documentation and incident examples.
