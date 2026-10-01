---
title: Windows Network Troubleshooting
source: Microsoft Learn
url: https://learn.microsoft.com/en-us/windows-server/networking/troubleshoot/troubleshoot-tcpip
product: Windows
topic: Network Troubleshooting
---

# Windows Network Troubleshooting

Windows network diagnosis should distinguish local adapter state, addressing, routing, name resolution, and application port access. `ipconfig /all` shows interface addresses, gateways, and DNS servers. `ping` can check basic IP reachability, while `tracert` can help show where a route stops. `Test-NetConnection` can test a specific TCP port and report name resolution and route information.

## Troubleshooting sequence

1. Check the adapter state and address with `ipconfig /all`.
2. Confirm the default gateway and DNS servers are expected.
3. Resolve the target hostname and compare the address with a known-good client.
4. Test the exact service port with `Test-NetConnection`.
5. Compare behavior from another network location.
6. Review Windows Firewall, VPN routes, and recent network profile changes.

A successful name lookup does not guarantee that the service port is reachable. A failed ping does not necessarily mean the application is down because ICMP may be filtered. Capture the exact command result, target, and timestamp so the network team can compare it with firewall or server logs.
