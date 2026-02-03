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

1. Describe node <node-name> to confirm DiskPressure condition, see the threshold that triggered it, check allocatable resources, and review recent events showing pod evictions.

2. Retrieve events for node <node-name> sorted by timestamp to identify when disk pressure started, which pods were evicted, and narrow down which pods may be causing the issue.

3. Retrieve events across all namespaces filtered by reason Evicted and sorted by timestamp to identify evicted pods - these pods are likely the largest disk consumers or victims that can help narrow down the cause.

4. SSH to the affected node and check disk usage: overall filesystem usage and inode usage (can cause DiskPressure even with space available).

5. Check /var/log on the affected node for accumulated logs that may be consuming disk space, including total log directory size, pod logs specifically, and largest log files.

6. Check cached container images consuming disk on the affected node: list all cached images, calculate total image size, and check container storage directories depending on runtime.

7. Check for orphaned resources consuming disk on the affected node: unused images compared with running containers, exited containers that have not been garbage collected, and orphaned pod directories.

8. Check kubelet garbage collection settings by examining kubelet config for imageGCHighThresholdPercent (default 85%) and imageGCLowThresholdPercent (default 80%) to understand eviction thresholds.

9. Check for log rotation issues on the affected node to identify unrotated logs and journal disk usage.

## Diagnosis

1. Analyze node events from Playbook step 2 to identify which pods were evicted and narrow down the primary disk consumers. Events showing "Evicted" with reason "DiskPressure" indicate immediate storage exhaustion. If multiple pods were evicted in rapid succession, the issue is likely acute disk exhaustion rather than gradual accumulation.

2. If events identify specific pods as heavy disk consumers, correlate those pod creation/restart timestamps with the DiskPressure condition transition time from Playbook step 1. The evicted pods are likely the largest disk consumers if they were created or restarted shortly before disk pressure began.

3. If events indicate image pull activity (reason="Pulled" from Playbook step 2-3), correlate image pull timestamps with disk pressure onset to determine if new container images triggered the issue. A surge of image pulls preceding DiskPressure suggests container image cache as the primary consumer.

4. If events show deployment or scaling activity, cross-reference with the log directory sizes from Playbook step 5. If /var/log/pods shows large sizes for recently deployed pods, application log accumulation is the likely cause.

5. If events are inconclusive, analyze the disk usage breakdown from Playbook steps 4-7:
   - If /var/lib/containers or image cache (step 6) dominates usage, check kubelet garbage collection thresholds from step 8 against current usage.
   - If /var/log dominates (step 5), check log rotation status from step 9.
   - If orphaned resources exist (step 7), container runtime cleanup failures are the cause.

6. If no single large consumer is identified, compare overall disk usage trends with deployment/scaling events from the past 1 hour to identify gradual accumulation from multiple sources.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review disk usage trends over a longer period to identify gradual growth, check for delayed effects from image pulls or log accumulation, examine container runtime storage usage patterns, verify if eviction thresholds were recently modified, and check for background processes or log rotation failures that may have started earlier. Disk pressure may accumulate gradually before triggering evictions.

