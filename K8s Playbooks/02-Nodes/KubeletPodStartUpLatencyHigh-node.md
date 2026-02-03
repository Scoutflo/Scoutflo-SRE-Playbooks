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

1. Describe node <node-name> to see:
   - Conditions section showing Ready status and DiskPressure condition
   - Events section showing any pod startup or performance issues
   - Allocated resources and current usage

2. Retrieve events for node <node-name> sorted by timestamp to see the sequence of node issues that may relate to pod startup latency.

3. Retrieve metrics for kubelet pod startup latency on the Node <node-name> to verify current latency values and identify performance issues.

4. Retrieve kubelet logs from the Node <node-name> by accessing via Pod Exec tool or SSH if node access is available, and filter for pod startup-related patterns to identify startup delays.

5. Retrieve metrics for the Node <node-name> and check node storage I/O metrics including IOPS, throughput, and latency to identify storage performance issues.

6. Verify container image pull times and image pull performance on the Node <node-name> to identify image pull delays.

7. Retrieve metrics for the Node <node-name> and check node resource usage including CPU, memory, and disk to identify resource constraints.

## Diagnosis

1. Analyze node events from Playbook steps 1-2 to identify pod startup issues. Events showing "FailedCreatePodSandBox", "ImagePullBackOff", or "ContainerCreating" delays indicate specific startup bottlenecks. Note event timestamps and affected pods.

2. If node events indicate DiskPressure condition, check node conditions from Playbook step 1 and correlate with storage I/O metrics from Playbook step 5. Disk pressure and IOPS exhaustion directly cause slow pod startup as container filesystem operations are delayed.

3. If node events show image pull delays ("Pulling image" events with long durations), verify image pull performance from Playbook step 6. Slow image pulls from registry, large image sizes, or network bandwidth constraints cause startup latency.

4. If node events indicate container runtime issues, check kubelet logs from Playbook step 4 for container runtime errors or slow operations. Container runtime performance degradation affects all pod lifecycle operations.

5. If pod startup latency metrics from Playbook step 3 show consistent high values, check node resource usage from Playbook step 7. CPU or memory constraints can cause slow container initialization and startup.

6. If startup latency is correlated with high pod density, compare current pod count with normal levels. High pod density increases container runtime overhead and PLEG processing time, indirectly affecting startup latency.

7. If startup latency is intermittent rather than consistent, check for resource contention patterns during peak usage periods or when many pods start simultaneously (such as during deployments or node recovery).

**If no root cause is identified from events**: Review container runtime logs for performance issues, check storage subsystem health and IOPS limits, verify network connectivity to container registries, and examine if node hardware (disk, memory) is degraded or undersized for the workload.
