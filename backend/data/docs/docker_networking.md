---
title: Docker Container Networking
source: Docker Documentation
url: https://docs.docker.com/engine/network/
product: Docker
topic: Container Networking
---

# Docker Container Networking

Containers communicate through Docker networks. On a user-defined bridge network, containers can use the other container's name as a hostname. `localhost` inside a container refers to that same container, not to another container or to the Docker host. This distinction commonly explains application-to-database connection failures.

A service must listen on the expected container port, and both containers must share a network that permits the connection. Publishing a port with `-p HOST_PORT:CONTAINER_PORT` makes a container port reachable from the host or configured external path; it is not required for two containers on the same user-defined network to communicate directly.

## Troubleshooting sequence

1. List networks with `docker network ls`.
2. Inspect the network and confirm both containers are attached.
3. Confirm the application uses the database or service name, not an incorrect `localhost` value.
4. Check the target process's listening port inside its container.
5. Review container logs and test resolution from the calling container.
6. Verify published ports only when host access is required.

The network name, service name, container port, and host port are different concepts. Record which one appears in the error. Avoid exposing a database port externally merely to make container-to-container communication work.
