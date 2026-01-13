---
title: Kubelet Pod Start Up Latency High
weight: 20
---

# KubeletPodStartUpLatencyHigh

## Meaning

Kubelet pod startup 99th percentile latency is exceeding thresholds on a node (triggering KubeletPodStartUpLatencyHigh alerts) because pods are taking too long to start, typically due to exhausted I/O operations per second (IOPS) for node storage, container image pull delays, or resource constraints. Kubelet pod startup latency metrics show high values exceeding thresholds, node storage I/O metrics indicate IOPS exhaustion, and node conditions may show DiskPressure. This affects the data plane and indicates node performance issues that delay pod startup and workload availability, typically caused by storage performance degradation, slow image pulls, or disk pressure; applications take longer to become available.

## Impact

KubeletPodStartUpLatencyHigh alerts fire; slow pod starts; pod startup latency exceeds thresholds; applications take longer to become available; pod scheduling to ready time is extended; node performance is degraded; container runtime operations are slow; pod startup operations take significantly longer than expected. Kubelet pod startup latency metrics show sustained high values; node storage I/O metrics indicate IOPS exhaustion; applications take significantly longer to become available; pod scheduling to ready time is extended; applications may experience delayed startup or performance degradation.

## Playbook

1. Retrieve metrics for kubelet pod startup latency on the Node `<node-name>` to verify current latency values and identify performance issues.

2. Retrieve kubelet logs from the Node `<node-name>` by accessing via Pod Exec tool or SSH if node access is available, and filter for pod startup-related patterns to identify startup delays.

3. Retrieve metrics for the Node `<node-name>` and check node storage I/O metrics including IOPS, throughput, and latency to identify storage performance issues.

4. Verify container image pull times and image pull performance on the Node `<node-name>` to identify image pull delays.

5. Retrieve metrics for the Node `<node-name>` and check node resource usage including CPU, memory, and disk to identify resource constraints.

6. Retrieve the Node `<node-name>` and verify node conditions including DiskPressure that may affect pod startup performance.

## Diagnosis

Compare pod startup latency increase timestamps with node storage I/O exhaustion detection times within 5 minutes and verify whether latency increased when storage IOPS were exhausted, using storage I/O metrics and pod startup latency as supporting evidence.

Correlate pod startup latency spikes with container image pull duration increases within 10 minutes and verify whether slow image pulls caused startup latency increases, using image pull metrics and pod startup times as supporting evidence.

Compare pod startup latency with node DiskPressure condition transitions within 5 minutes and verify whether disk pressure caused slow pod starts, using node conditions and pod startup latency as supporting evidence.

Analyze pod startup latency patterns over the last 15 minutes to determine if latency is consistently high (storage issue) or intermittent (resource constraints), using pod startup latency metrics and node resource usage as supporting evidence.

Correlate pod startup latency with pod density increases on node `<node-name>` within 30 minutes and verify whether high pod density caused startup delays, using pod density metrics and pod startup latency as supporting evidence.

Compare current pod startup latency with historical baseline latency for node `<node-name>` over the last 7 days and verify whether current latency represents a new issue or ongoing performance problems, using pod startup latency history and node performance baselines as supporting evidence.

If no correlation is found within the specified time windows: extend timeframes to 1 hour for performance analysis, review container runtime configuration, check for storage performance degradation, verify node hardware health, examine historical pod startup performance patterns. Pod startup latency may be high due to storage performance issues, image pull delays, or node resource constraints rather than immediate changes.
