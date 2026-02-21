---
title: Node High Memory Usage
weight: 31
categories: [kubernetes, node]
---

# NodeHighMemoryUsage

## Meaning

Node is experiencing high memory utilization (triggering NodeHighMemoryUsage, NodeMemoryHighUtilization alerts, typically when memory usage exceeds 80-90%) because the node's RAM is heavily utilized by running pods, system caches, or kernel buffers. Node metrics show high memory utilization, available memory is low, and the node may be at risk of OOM conditions. This affects the node and all workloads running on it; pods may be evicted or OOMKilled; new pod scheduling is restricted; system stability is at risk.

## Impact

NodeHighMemoryUsage alerts fire; pods risk OOMKill from kubelet eviction; new pods cannot be scheduled to this node; system may become unresponsive; swap usage increases if enabled; kernel may invoke OOM killer; critical system processes may be affected; kubelet may evict pods based on memory pressure; service disruption across multiple applications; node may become NotReady.

## Playbook

1. Retrieve the Node `<node-name>` and verify current memory utilization, available memory, and MemoryPressure condition.

2. Retrieve all pods running on the node and identify which pods are consuming the most memory using container_memory_working_set_bytes metrics.

3. Distinguish between actual memory usage and cache/buffers (which can be reclaimed) to understand true memory pressure.

4. Check for pods without memory limits that may be consuming excessive resources.

5. Retrieve node eviction thresholds (kubelet configuration) and verify how close the node is to triggering evictions.

6. Check for system processes (outside containers) consuming significant memory.

7. Verify if the node has appropriate memory for its workload mix.

## Diagnosis

Compare pod memory usage with limits and verify whether specific pods are approaching or exceeding limits, causing node-wide pressure, using container metrics and resource specs as supporting evidence.

Analyze memory composition (working set vs cache vs buffers) and verify whether high memory is due to application data (concerning) or reclaimable caches (less concerning), using detailed memory metrics as supporting evidence.

Correlate memory increase with recent deployments and verify whether new workloads or updated versions introduced memory regression, using deployment timestamps and memory trends as supporting evidence.

Check for memory leaks in specific containers by identifying pods with continuously growing memory usage, using long-term memory trends and restart history as supporting evidence.

Verify if eviction thresholds are configured appropriately and whether kubelet should be evicting pods earlier to protect node stability, using kubelet configuration and eviction events as supporting evidence.

If no correlation is found within the specified time windows: identify and restart pods with memory leaks, add or increase memory limits on pods, consider draining node to redistribute workload, review node instance sizing, check for kernel memory leaks or driver issues.
