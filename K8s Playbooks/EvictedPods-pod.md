---
title: Evicted Pods - Pod
weight: 205
categories:
  - kubernetes
  - pod
---

# EvictedPods-pod

## Meaning

Pods are being forcibly evicted by the kubelet from a node because resource pressure thresholds (MemoryPressure, DiskPressure conditions triggering KubeNodeMemoryPressure or KubeNodeDiskPressure alerts) have been exceeded. Pods show Evicted state in kubectl, pod status reason shows Evicted with resource pressure type, and node conditions show MemoryPressure or DiskPressure. This affects the workload plane and indicates node resource exhaustion, typically caused by memory or disk pressure; applications experience unexpected restarts and may show errors.

## Impact

Pods are forcibly terminated; applications experience unexpected restarts; deployments lose replicas; services may become unavailable; applications may lose in-memory state; pod eviction events occur; node pressure conditions trigger alerts; pod status changes to Evicted; resource constraints prevent pod scheduling. Pods show Evicted state indefinitely; pod status reason shows Evicted with resource pressure type; applications experience unexpected restarts and may show errors; applications may lose in-memory state.

## Playbook

1. List pods in namespace `<namespace>` and filter for pods with `status.reason="Evicted"`, then retrieve each affected pod to examine the eviction reason and message.

2. List all nodes and retrieve CPU, memory, and disk usage metrics to identify nodes operating under significant resource pressure.

3. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review container resource requests and limits to confirm they are appropriate for node capacities.

4. Retrieve each affected node `<node-name>` and inspect node conditions such as `MemoryPressure` and `DiskPressure` to confirm the type of pressure causing evictions.

5. Review pod resource usage metrics for evicted workloads to determine whether they were consuming excessive memory, CPU, or disk relative to limits or expectations.

## Diagnosis

1. Compare the pod eviction timestamps (when pods were marked as Evicted) with node MemoryPressure and DiskPressure condition transition times, and check whether resource pressure is reported within 5 minutes of evictions.

2. Compare the pod eviction timestamps with node resource usage metrics (CPU, memory, and disk) and check whether spikes or sustained high utilization occur within 5 minutes of the evictions.

3. Compare the pod eviction timestamps with Deployment resource request changes and check whether raising resource requests within the previous 1 hour correlates with increased evictions.

4. Compare the pod eviction timestamps with Deployment or scaling event timestamps (for example, `ScalingReplicaSet` events) and check whether large scale-ups occurred within 30 minutes before the evictions began.

5. Compare the pod eviction timestamps with node capacity information and any changes to node pool size, and check whether reductions in capacity or node removal align with eviction periods.

6. Compare the pod eviction timestamps with cluster scaling operations and node maintenance windows, and check whether evictions started within 1 hour of those activities.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 1 hour → 2 hours), review node resource metrics over a longer period to identify gradual pressure buildup, check for delayed effects from resource request changes, examine node capacity reductions that occurred earlier, and verify if eviction thresholds were recently modified. Resource pressure may accumulate gradually before triggering evictions.

