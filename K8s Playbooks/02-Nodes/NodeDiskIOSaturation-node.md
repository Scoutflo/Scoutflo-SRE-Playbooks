---
title: Node Disk IO Saturation
weight: 33
categories: [kubernetes, node]
---

# NodeDiskIOSaturation

## Meaning

Node disk I/O is saturated (triggering NodeDiskIOSaturation alerts) because the disk subsystem is handling more I/O operations than it can efficiently process, causing I/O wait and latency. Node metrics show high I/O wait time, disk queue depth is elevated, and I/O operations experience significant latency. This affects all workloads on the node performing disk operations; database performance degrades; log writes are delayed; container startup slows; applications experience timeouts.

## Impact

NodeDiskIOSaturation alerts fire; all disk operations slow down; database queries timeout; log writes are delayed; container image pulls slow; application response times increase; I/O-bound operations queue up; CPU shows high iowait percentage; system appears sluggish; fsync operations block; write-heavy workloads suffer; container startup times increase.

## Playbook

1. Retrieve the Node `<node-name>` and verify disk I/O metrics including iowait, disk utilization, and queue depth.

2. Identify which disk device is saturated and which filesystem it serves (/var/lib/docker, /var/lib/kubelet, data volumes).

3. Retrieve pods running on the node and identify which pods are generating the most disk I/O.

4. Check for database or log-heavy workloads that may be causing excessive disk writes.

5. Verify if the disk type (HDD vs SSD vs NVMe) is appropriate for the workload I/O patterns.

6. Check for disk performance degradation in cloud environments (throttling due to burst credits exhaustion).

7. Review PersistentVolumes attached to the node and their I/O characteristics.

## Diagnosis

Compare disk I/O patterns with workload activity and verify whether specific pods are generating excessive I/O, using per-container I/O metrics and pod activity as supporting evidence.

Analyze I/O pattern type (sequential vs random, read vs write) and verify whether the disk type is appropriate for the workload pattern, using I/O metrics and disk specifications as supporting evidence.

Correlate I/O saturation with cloud disk throttling (IOPS limits, throughput limits, burst credits) and verify whether cloud disk limits are being exceeded, using cloud provider metrics and disk tier configuration as supporting evidence.

Check for log rotation issues or excessive logging that creates write amplification, using log file sizes and write patterns as supporting evidence.

Verify if container image pulls or builds are causing temporary I/O spikes, using kubelet activity and image pull events as supporting evidence.

If no correlation is found within the specified time windows: upgrade disk to faster tier (SSD/NVMe), increase disk IOPS limits in cloud, distribute I/O across multiple disks, move log-heavy workloads to separate disk, implement log rate limiting, consider node with local NVMe storage.
