---
title: Linux File Permissions Troubleshooting
source: Ubuntu Documentation
url: https://documentation.ubuntu.com/desktop/en/latest/tutorial/file-permissions/
product: Linux / Ubuntu
topic: File Permissions
---

# Linux File Permissions Troubleshooting

Linux file access is evaluated using an owning user, an owning group, and permission bits for the owner, group, and others. `ls -l path` shows ownership and mode. A service may fail even when an administrator can read a file, because the service runs as a different account and may also need execute permission on every parent directory.

When an application reports `Permission denied`, identify the account running the process and inspect the target file and its parent directories. Confirm whether the operation needs read, write, or execute access. Do not solve an application problem by making a file world-writable or running the service as root.

## Troubleshooting checklist

1. Identify the process account from the service definition or process list.
2. Inspect ownership and permissions with `ls -l` and `namei -l`.
3. Check whether a parent directory blocks traversal.
4. Compare the path with the application's configured path.
5. Restore the narrow, approved owner/group and mode.
6. Retry the original operation and inspect the application log.

Configuration files, upload directories, log directories, and deployment paths often need different ownership. Make the smallest permission change that matches the intended service design, and record the path and account involved without recording secrets or private file contents.
