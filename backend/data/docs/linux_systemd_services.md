---
title: Linux systemd Service Troubleshooting
source: Ubuntu Documentation
url: https://documentation.ubuntu.com/server/explanation/systemd/service-management/
product: Linux / Ubuntu
topic: systemd Services
---

# Linux systemd Service Troubleshooting

`systemd` manages many Linux services. `systemctl status service-name` shows whether a service is active, failed, or stopped and includes recent status information. `systemctl start`, `stop`, `restart`, and `reload` perform the corresponding service operations when permitted. `systemctl enable` configures a service to start during boot; it does not start the service immediately unless `--now` is also used.

For more detail, use `journalctl -u service-name` to inspect the service journal. The journal often contains the first useful error, such as a missing file, invalid configuration, permission failure, unavailable dependency, or occupied port.

## Troubleshooting sequence

1. Run `systemctl status service-name`.
2. Read recent entries with `journalctl -u service-name --since ...`.
3. Validate the service configuration using the product's validation command.
4. Check paths, ownership, dependencies, and listening ports.
5. Apply the smallest approved correction and restart or reload the service.
6. Verify the service and its health endpoint after the change.

A service that is `enabled` can still be `failed`, and a service that is `active` can still expose an application-level failure. Treat the service status, journal, and application health check as separate observations.
