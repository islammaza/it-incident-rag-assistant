---
title: Nginx Reverse Proxy and Upstream Troubleshooting
source: Nginx Documentation
url: https://nginx.org/en/docs/http/ngx_http_proxy_module.html
product: Nginx
topic: Reverse Proxy and Upstreams
---

# Nginx Reverse Proxy and Upstream Troubleshooting

Nginx forwards requests to an upstream server with the `proxy_pass` directive. The proxy location, upstream hostname, port, URI handling, and request headers must match the application contract. A syntactically valid Nginx configuration can still point to the wrong service or path.

Use `nginx -t` before reloading a configuration. Inspect the active server block and confirm the `server_name` selected for the request. When Nginx returns 502 or 504, compare the configured upstream with the application's actual listening address and port.

## Diagnostic sequence

1. Validate syntax with `nginx -t`.
2. Read the Nginx error log for the upstream endpoint and reason.
3. Check the application service status and listening socket.
4. Test the upstream locally from the Nginx host when permitted.
5. Verify DNS, path rewriting, protocol, and timeout settings.
6. Reload only after validation, then test through the public proxy path.

`connection refused` usually means the target address has no accepting listener. A timeout can indicate network filtering or a slow upstream. Keep proxy configuration changes narrow and preserve the previous known-good configuration for rollback.
