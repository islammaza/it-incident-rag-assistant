---
title: Linux CPU and Memory Troubleshooting
source: Ubuntu Documentation
url: https://documentation.ubuntu.com/server/how-to/monitor-your-system/system-monitoring/
product: Linux / Ubuntu
topic: CPU and Memory
---

# Linux CPU and Memory Troubleshooting

High CPU and memory usage should be tied to a process and a time window before changing configuration. Tools such as `top`, `htop`, `ps`, `free`, and `vmstat` show current resource pressure. Compare the observation with application metrics and recent deployments rather than assuming that high utilization alone is the root cause.

A process consuming CPU can indicate normal workload, a stuck worker, a retry loop, or a runaway diagnostic setting. Memory pressure can cause swapping, slow responses, or an out-of-memory kill. Review kernel messages and service logs when a process disappears unexpectedly.

## Troubleshooting sequence

- Record load average, CPU usage, memory, swap, and the top processes.
- Check whether the behavior is constant or tied to a request, job, or deployment.
- Inspect application worker counts, queue depth, and recent configuration changes.
- Review logs for repeated retries, allocation failures, or OOM messages.
- Stop or restart only the affected process when an approved procedure exists.
- Verify resource usage and application response after the correction.

Do not increase memory limits blindly. A larger limit can move pressure to the host, while a smaller worker count or bounded queue may address the actual cause. Preserve timestamps and process names in incident notes so later diagnosis can compare similar events.
