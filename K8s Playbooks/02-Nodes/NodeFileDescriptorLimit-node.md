---
title: Node File Descriptor Limit
weight: 36
categories: [kubernetes, node]
---

# NodeFileDescriptorLimit

## Meaning

Node is approaching or exceeding file descriptor limits (triggering NodeFileDescriptorLimit, NodeFileDescriptorsExhaustion alerts) because the number of open files, sockets, and pipes is approaching system limits. Node metrics show high file descriptor utilization, new connections fail, and processes cannot open files. This affects all workloads on the node; network connections fail; file operations fail; container creation fails; system becomes unstable.

## Impact

NodeFileDescriptorLimit alerts fire; new socket connections fail with "too many open files"; file open operations fail; container creation may fail; kubelet operations are affected; database connections cannot be established; log files cannot be opened; network services stop accepting connections; existing connections may be forcibly closed; system stability degrades.

## Playbook

1. Retrieve the Node `<node-name>` and verify current file descriptor usage versus limits (node_filefd_allocated, node_filefd_maximum).

2. Identify processes consuming the most file descriptors using lsof or /proc/<pid>/fd counts.

3. Check for pods or containers with file descriptor leaks (connections not being closed).

4. Verify system-wide limits in /etc/sysctl.conf (fs.file-max) and per-process limits in /etc/security/limits.conf.

5. Check kubelet and container runtime file descriptor usage.

6. Identify long-running pods that may be accumulating file descriptors over time.

7. Verify application connection pooling is properly configured and connections are being returned.

## Diagnosis

Identify top file descriptor consumers and verify whether specific processes are leaking descriptors, using per-process fd counts and process identification as supporting evidence.

Correlate file descriptor growth with uptime and verify whether descriptors accumulate over time indicating leak, versus staying stable at high level indicating legitimate usage, using fd count trends and process restart history as supporting evidence.

Check for socket accumulation in TIME_WAIT, CLOSE_WAIT states indicating connection handling issues, using netstat output and connection state analysis as supporting evidence.

Verify application connection pool configuration and confirm connections are properly bounded and released, using application configuration and connection metrics as supporting evidence.

Compare with other nodes and verify whether the issue is specific to certain workloads on this node, using cross-node comparison and workload placement as supporting evidence.

If no correlation is found within the specified time windows: increase fs.file-max system limit, increase per-process limits for affected services, restart pods with file descriptor leaks, review and fix application connection handling, implement connection timeouts and cleanup.
