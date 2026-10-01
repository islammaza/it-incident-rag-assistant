---
title: Linux Disk Space Troubleshooting
source: Ubuntu Documentation
url: https://documentation.ubuntu.com/server/how-to/monitor-your-system/disk-space/
product: Linux / Ubuntu
topic: Disk Space
---

# Linux Disk Space Troubleshooting

A full filesystem can prevent applications from writing logs, temporary files, sockets, or database files. Start with `df -h` to see capacity by mounted filesystem. Use `du` on the affected mount to identify directories consuming space, while avoiding unrelated mounts and sensitive file contents.

The filesystem with available space is important: freeing space on `/home` does not fix a full `/var`, and freeing space on the root filesystem does not necessarily fix a separate database volume. Check inode usage with `df -i` when files appear small but creation still fails.

## Diagnostic approach

- Identify the exact mount reported in the error.
- Compare used space with recent application, system, and container log growth.
- Check whether log rotation is configured and operating.
- Look for old, approved temporary files or artifacts.
- Check for deleted files still held open by a process if usage does not match visible files.
- Make a controlled cleanup, then verify application writes.

Do not delete active database files, arbitrary logs, or unknown application data. Prefer the application's retention mechanism, log rotation, or an approved archive procedure. After cleanup, confirm both free space and the original operation, because a service may need a restart or retry.
