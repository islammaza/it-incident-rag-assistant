---
title: HTTP 503 Service Unavailable
source: MDN Web Docs
url: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status/503
product: HTTP / Web
topic: HTTP 503
---

# HTTP 503 Service Unavailable

HTTP status `503 Service Unavailable` indicates that the server is currently not ready to handle the request, commonly because of temporary overload or maintenance. The response may include `Retry-After`, but clients should not treat retries as a fix when the service remains unhealthy.

## Troubleshooting approach

- Determine whether the response comes from the application, reverse proxy, load balancer, or maintenance layer.
- Check service health, readiness checks, worker capacity, and dependency availability.
- Inspect deployment and maintenance events around the first failure.
- Review logs for exhausted connections, unavailable upstreams, startup failures, and resource pressure.
- Confirm whether only new instances are failing or all instances are affected.
- Verify recovery with the documented health endpoint and a representative request.

A 503 differs from a 502: 503 means the responding service is unavailable or not ready, while 502 describes an invalid response from an upstream gateway target. Keep the observed status, response headers, proxy route, and timestamp in incident notes.
