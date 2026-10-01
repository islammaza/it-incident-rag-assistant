---
title: Docker Container Logs
source: Docker Documentation
url: https://docs.docker.com/engine/logging/
product: Docker
topic: Container Logs
---

# Docker Container Logs

Docker captures output written to a container's standard output and standard error through a logging driver. `docker logs CONTAINER` displays available output; `--since`, `--until`, and `--tail` help narrow a noisy incident. Logs are useful for startup failures, repeated exceptions, missing settings, and dependency connection errors.

The exact output and retention behavior depends on the configured logging driver. A containerized application that writes only to files inside the container may not appear in `docker logs`; in that case, inspect the application's configured log destination according to its documented procedure.

## Troubleshooting sequence

1. Identify the exact container and its current state with `docker ps -a`.
2. Read recent output with `docker logs --tail 200 CONTAINER`.
3. Compare the first failure with later repeated messages.
4. Check the image, command, environment, mounts, and network configuration.
5. Correct the configuration or image, then recreate the container when appropriate.
6. Confirm logs show a healthy startup rather than only a running process.

Avoid putting credentials, tokens, or private request payloads into diagnostic notes. Container logs can also consume host disk space, so retention and rotation should be checked when disk alerts accompany container incidents.
