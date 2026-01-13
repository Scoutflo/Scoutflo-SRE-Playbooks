---
title: Pods Stuck in Evicted State - Pod
weight: 283
categories:
  - kubernetes
  - pod
---

# PodsStuckinEvictedState-pod

## Meaning

Pods remain in Evicted state (triggering KubePodNotReady alerts) because they were evicted by kubelet due to node resource pressure (MemoryPressure, DiskPressure, PIDPressure) but were not automatically cleaned up. Pods show Evicted state in kubectl, pod status reason shows Evicted with resource pressure type, and node conditions may show MemoryPressure, DiskPressure, or PIDPressure. This affects the workload plane and blocks cleanup, typically caused by node resource exhaustion; applications cannot run on affected nodes.

## Impact

Evicted pods remain in the cluster; pod resources are not released; deployments cannot achieve desired replica count; new pods may fail to schedule due to resource constraints; namespace cleanup is blocked; pod status shows Evicted state; KubePodNotReady alerts fire; node resources remain allocated to evicted pods; cluster resource management is impaired. Pods show Evicted state indefinitely; pod status reason shows Evicted with resource pressure type; node conditions show MemoryPressure, DiskPressure, or PIDPressure; applications cannot run on affected nodes and may show errors.

## Playbook

1. List pods in namespace `<namespace>` and filter for pods with status `Evicted` to identify all evicted pods.

2. Retrieve the pod `<pod-name>` in namespace `<namespace>` and inspect `status.reason` and `status.message` to confirm eviction reason and identify which resource pressure caused the eviction.

3. List events in namespace `<namespace>` and filter for eviction events, focusing on events with reasons such as `Evicted` and messages indicating the resource pressure type (memory, disk, PID).

4. Check the node where the pod was evicted and verify its resource pressure conditions (MemoryPressure, DiskPressure, PIDPressure) to understand current node state.

5. Retrieve the Deployment `<deployment-name>` in namespace `<namespace>` and review resource requests to verify if requests are reasonable relative to node capacity.

6. Check node resource usage metrics to verify current available resources and identify if node-level resource pressure persists.

## Diagnosis

1. Compare the pod eviction timestamps with node MemoryPressure condition transition timestamps, and check whether memory pressure occurred within 5 minutes before pod evictions.

2. Compare the pod eviction timestamps with node DiskPressure condition transition timestamps, and check whether disk pressure occurred within 5 minutes before pod evictions.

3. Compare the pod eviction timestamps with node resource usage metric spikes (CPU, memory, disk), and check whether resource exhaustion occurred within 5 minutes before evictions.

4. Compare the pod eviction timestamps with deployment resource request modification timestamps, and check whether resource requests were increased within 30 minutes before evictions, causing nodes to exceed capacity.

5. Compare the pod eviction timestamps with cluster scaling events or workload increases, and check whether resource competition increased within 30 minutes before evictions.

6. Compare the pod eviction timestamps with node maintenance, cordoning, or draining operations, and check whether node operations occurred within 1 hour before evictions, potentially causing resource pressure.

**If no correlation is found within the specified time windows**: Extend the search window (5 minutes → 10 minutes, 30 minutes → 1 hour, 1 hour → 2 hours), review node resource usage trends for gradual exhaustion, check for cumulative resource pressure from multiple workloads, examine if eviction thresholds were recently adjusted, verify if node capacity decreased due to other resource allocations, and check for gradual workload growth that exceeded node capacity over time. Pod evictions may result from cumulative resource pressure rather than immediate changes.

