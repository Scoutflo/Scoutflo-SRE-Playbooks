---
title: Node Disk Pressure - Storage
weight: 213
categories:
  - kubernetes
  - storage
---

# NodeDiskPressure-storage

## Meaning

A node has entered DiskPressure condition (triggering KubeNodeDiskPressure alerts) because available disk space or inodes have dropped below kubelet eviction thresholds, triggering pod evictions and making the node unsafe for new scheduling. Disk pressure causes kubelet to evict pods and mark the node as having insufficient storage resources.

## Impact

Pods are evicted from node; applications experience unexpected restarts; node becomes unschedulable; workloads are disrupted; data may be lost if pods are evicted before graceful shutdown; KubeNodeDiskPressure alerts fire; node condition shows DiskPressure; pod eviction events occur; node scheduling disabled due to disk pressure.

## Playbook

1. List all nodes and retrieve detailed information for each node to identify those reporting the `DiskPressure` condition.

2. On nodes with DiskPressure, check disk space and inode availability using `df -h` and related tools to see which filesystems are near capacity.

3. For each affected node, inspect node conditions to confirm `DiskPressure` and any related warnings or messages.

4. List pods across all namespaces and filter for pods with `status.reason="Evicted"` to understand which workloads are being removed due to disk pressure.

5. On affected nodes, measure disk usage for container image storage and log directories (for example, using `du` on `/var/lib/containers` and `/var/log`) to identify major disk consumers.

6. Review pod resource and volume usage metrics for workloads running on the affected nodes to determine whether any pods are causing unusual disk growth.

## Diagnosis

1. Compare the pod eviction timestamps for evicted pods with node DiskPressure condition transition times, and check whether DiskPressure is reported within 5 minutes of pod evictions.

2. Compare the pod eviction timestamps with disk space availability checks (for example, results of `df -h`) and container/log directory usage measurements (such as `du` on `/var/lib/containers` and `/var/log`), and check whether disk usage spikes or runs out around the time of the evictions.

3. Compare the pod eviction timestamps with container image pull event timestamps (events where `reason="Pulled"`), and check whether a surge of image pulls occurs within 30 minutes prior to the evictions.

4. Compare the pod eviction timestamps with log file growth or volume usage (for example, metrics for pod volumes and filesystem usage), and check whether rapid log or volume growth is observed around the time of evictions.

5. Compare the pod eviction timestamps with deployment or scaling event timestamps, and check whether large scale-ups or new deployments started within 1 hour before evictions began.

6. Compare the pod eviction timestamps with node maintenance or configuration change timestamps, and check whether evictions started within 1 hour of changes to node configuration, runtime settings, or storage.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review disk usage trends over a longer period to identify gradual growth, check for delayed effects from image pulls or log accumulation, examine container runtime storage usage patterns, verify if eviction thresholds were recently modified, and check for background processes or log rotation failures that may have started earlier. Disk pressure may accumulate gradually before triggering evictions.

