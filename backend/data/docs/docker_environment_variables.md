---
title: Docker Environment Variables
source: Docker Documentation
url: https://docs.docker.com/compose/how-tos/environment-variables/
product: Docker
topic: Environment Variables
---

# Docker Environment Variables

Containerized applications often receive non-secret runtime settings through environment variables. Compose can read values from the shell, an environment file, or an explicit `environment` section. The final value available inside the container should be verified because interpolation and precedence can differ between the host configuration and the container environment.

Missing variables frequently cause startup errors, while a wrong value can make an application connect to the wrong service or use the wrong mode. Inspect configuration structure and variable names without printing secrets. Use a sanitized or non-sensitive setting when demonstrating a diagnosis.

## Troubleshooting checklist

- Check the variable name expected by the application.
- Inspect the resolved Compose configuration when appropriate.
- Confirm the variable is present inside the running container.
- Compare non-sensitive values with the environment's approved configuration.
- Recreate the container after changing environment variables; a running process does not automatically receive new values.
- Review startup logs and the application health check.

Do not commit passwords, tokens, private keys, or populated secret files. Environment variables are configuration inputs, not a substitute for a secret-management policy. For this local knowledge base, only generic variable names and non-sensitive examples are used.
