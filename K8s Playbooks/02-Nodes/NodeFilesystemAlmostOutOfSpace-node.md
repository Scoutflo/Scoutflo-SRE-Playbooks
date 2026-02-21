---
title: Node Filesystem Almost Out of Space
weight: 32
categories: [kubernetes, node]
---

# NodeFilesystemAlmostOutOfSpace

## Meaning

Node filesystem is running low on disk space (triggering NodeFilesystemAlmostOutOfSpace, NodeDiskSpaceLow, NodeDiskSpaceCritical alerts, typically when usage exceeds 80-90%) because the disk is filling up with container images, logs, ephemeral storage, or persistent data. Node metrics show high filesystem utilization, available space is critically low, and the node may stop accepting new workloads. This affects the node and all workloads; pods may be evicted; new pods cannot be scheduled; container creation fails; logs cannot be written; system may become unstable.

## Impact

NodeFilesystemAlmostOutOfSpace alerts fire; new container images cannot be pulled; pods may be evicted due to DiskPressure; new pods cannot be scheduled to this node; container logs cannot be written; application writes fail; database operations fail if data is on this filesystem; kubelet marks node with DiskPressure condition; system services may fail; node may become NotReady; data corruption risk if disk fills completely.

## Playbook

1. Retrieve the Node `<node-name>` and verify current disk usage, available space, and DiskPressure condition.

2. Identify which filesystem is running low (/var/lib/docker, /var/lib/containerd, /var/log, /var/lib/kubelet).

3. Check container image cache size and identify unused images that can be garbage collected.

4. Retrieve pod ephemeral storage usage and identify pods consuming excessive local storage.

5. Check container log sizes and identify pods producing excessive logs.

6. Verify kubelet garbage collection settings for images and containers.

7. Check for PersistentVolumes using local storage on the node.

## Diagnosis

Analyze disk usage breakdown and identify whether space is consumed by container images, container logs, ephemeral storage, or system files, using disk usage analysis and file system inspection as supporting evidence.

Compare container image age and usage and verify whether old unused images are consuming space that garbage collection should reclaim, using image list and last-used timestamps as supporting evidence.

Correlate disk growth with specific pods and verify whether particular pods are writing excessive data to emptyDir or hostPath volumes, using pod ephemeral storage metrics as supporting evidence.

Check log file sizes and rotation configuration and verify whether log files are growing unbounded due to missing log rotation, using log file sizes and rotation configuration as supporting evidence.

Verify if kubelet eviction thresholds are configured correctly and whether imagefs or nodefs is under pressure, using kubelet configuration and eviction events as supporting evidence.

If no correlation is found within the specified time windows: manually remove unused container images, compress or delete old logs, clean up crashed container data, increase disk size if in cloud environment, review and set pod ephemeral storage limits.
