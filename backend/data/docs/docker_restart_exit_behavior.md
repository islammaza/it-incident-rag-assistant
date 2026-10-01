---
title: Docker Container Restart and Exit Behavior
source: Docker Documentation
url: https://docs.docker.com/engine/containers/start-containers-automatically/
product: Docker
topic: Restart Policies and Exit Codes
---

# Docker Container Restart and Exit Behavior

A container stops when its main process exits. `docker ps -a` shows stopped containers, their exit status, and the command that was run. An exit code is a symptom of the process result, not a complete diagnosis; the container logs and image command explain why it stopped.

Docker restart policies control whether a container is restarted after it exits or after the Docker daemon starts. Common policies include `no`, `on-failure`, `always`, and `unless-stopped`. A restart policy can make a failed application appear as a restart loop, so inspect the current status and recent logs before changing it.

## Troubleshooting checklist

- Run `docker ps -a` and note status, restart count, and exit code.
- Read the first startup error with `docker logs`.
- Inspect the image entrypoint and command.
- Verify required mounts, environment variables, files, and network dependencies.
- Check whether the restart policy is masking a deterministic startup failure.
- Recreate the container only after correcting the underlying input.

A healthy container process does not guarantee a healthy application. Use the application's health endpoint or a documented health check after startup. Do not use an infinite restart policy to hide a configuration or dependency failure.
