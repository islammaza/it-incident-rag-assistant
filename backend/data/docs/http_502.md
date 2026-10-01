---
title: HTTP 502 Bad Gateway
source: MDN Web Docs
url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/502
product: HTTP / Web
topic: HTTP 502
---

# HTTP 502 Bad Gateway

HTTP status `502 Bad Gateway` means a gateway or proxy received an invalid response from an upstream server. In a common reverse-proxy setup, the proxy is reachable but cannot successfully communicate with the application service behind it.

## Troubleshooting approach

1. Confirm the proxy process is running and serving the expected host.
2. Inspect proxy error logs for the upstream address and failure reason.
3. Check whether the upstream application process is running and listening on the configured port.
4. Test the upstream locally from the proxy host when permitted.
5. Verify DNS, network access, protocol, and proxy path settings.
6. Review the upstream application's startup and error logs.

`Connection refused` often indicates that no process is listening at the configured upstream endpoint. A timeout points more toward routing, firewall, or an overloaded upstream. A malformed response can indicate an upstream protocol mismatch or an application failure. Correct the layer that produced the failure, then test through the same proxy hostname and path.
